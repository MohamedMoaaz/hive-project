import csv
import os
import subprocess
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
from io import StringIO

class PostgresToHdfsExporter:
    def __init__(self, pg_config, hdfs_path, tables, hdfs_container, container_temp_dir):
        """
        Initialize the exporter with configuration parameters.
        
        Args:
            pg_config (dict): PostgreSQL connection parameters
            hdfs_path (str): Base HDFS path where tables will be stored
            tables (list): List of tables to export
            hdfs_container (str): Name of the HDFS container (Docker container name)
            container_temp_dir (str): Temporary directory inside the container for staging files
        """
        self.pg_config = pg_config
        self.hdfs_path = hdfs_path
        self.tables = tables
        self.hdfs_container = hdfs_container
        self.container_temp_dir = container_temp_dir
        
        # Ensure temp dir ends with a slash
        if not self.container_temp_dir.endswith('/'):
            self.container_temp_dir += '/'
    
    def _get_postgres_connection(self):
        """Establish a connection to PostgreSQL."""
        return psycopg2.connect(
            host=self.pg_config['host'],
            port=self.pg_config['port'],
            dbname=self.pg_config['dbname'],
            user=self.pg_config['user'],
            password=self.pg_config['password']
        )
    
    def _export_table_to_csv(self, table_name):
        """
        Export a PostgreSQL table to a CSV file in the container's temp directory.
        
        Args:
            table_name (str): Name of the table to export
            
        Returns:
            str: Path to the generated CSV file in the container
        """
        # Create a CSV file in the container's temp directory
        csv_filename = f"{table_name}.csv"
        container_csv_path = os.path.join(self.container_temp_dir, csv_filename)
        
        # Connect to PostgreSQL
        conn = self._get_postgres_connection()
        cursor = conn.cursor()
        
        try:
            # Create a StringIO buffer to hold CSV data
            csv_buffer = StringIO()
            
            # Execute query and get column names
            cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            colnames = [desc[0] for desc in cursor.description]
            
            # Create CSV writer
            csv_writer = csv.writer(csv_buffer)
            csv_writer.writerow(colnames)
            
            # Fetch data and write to CSV
            while True:
                rows = cursor.fetchmany(size=1000)
                if not rows:
                    break
                csv_writer.writerows(rows)
            
            # Write CSV data to a temporary file on host
            host_temp_dir = '/tmp/csv_staging'
            os.makedirs(host_temp_dir, exist_ok=True)
            host_csv_path = os.path.join(host_temp_dir, csv_filename)
            
            with open(host_csv_path, 'w') as f:
                f.write(csv_buffer.getvalue())
            
            # Copy file from host to container
            subprocess.run([
                'docker', 'cp', 
                host_csv_path, 
                f"{self.hdfs_container}:{container_csv_path}"
            ], check=True)
            
            # Clean up host temp file
            os.remove(host_csv_path)
            
            return container_csv_path
            
        finally:
            cursor.close()
            conn.close()
    
    def _load_csv_to_hdfs(self, table_name, container_csv_path):
        """
        Load a CSV file from the container to HDFS.
        
        Args:
            table_name (str): Name of the table being exported
            container_csv_path (str): Path to CSV file in the container
            
        Returns:
            bool: True if successful, False otherwise
        """
        hdfs_table_path = os.path.join(self.hdfs_path, table_name)
        
        try:
            # Create HDFS directory if it doesn't exist
            subprocess.run([
                'docker', 'exec', self.hdfs_container,
                'hdfs', 'dfs', '-mkdir', '-p', hdfs_table_path
            ], check=True)
            
            # Copy file from container local to HDFS
            subprocess.run([
                'docker', 'exec', self.hdfs_container,
                'hdfs', 'dfs', '-put',
                '-f', container_csv_path,
                hdfs_table_path
            ], check=True)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error loading {table_name} to HDFS: {e}")
            return False
        finally:
            # Clean up the CSV file in the container
            subprocess.run([
                'docker', 'exec', self.hdfs_container,
                'rm', '-f', container_csv_path
            ], check=False)
    
    def export_tables(self):
        """
        Export all configured tables from PostgreSQL to HDFS.
        
        Returns:
            dict: Dictionary with table names as keys and status messages as values
        """
        results = {}
        
        for table in self.tables:
            try:
                print(f"Exporting table: {table}")
                
                # Step 1: Export table to CSV in container
                container_csv_path = self._export_table_to_csv(table)
                
                # Step 2: Load CSV to HDFS
                success = self._load_csv_to_hdfs(table, container_csv_path)
                
                results[table] = "SUCCESS" if success else "FAILED"
                
            except Exception as e:
                results[table] = f"FAILED: {str(e)}"
                print(f"Error exporting table {table}: {e}")
        
        return results