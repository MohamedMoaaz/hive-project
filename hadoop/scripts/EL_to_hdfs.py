import os
import psycopg2
import pandas as pd
import subprocess

class PostgresToHdfsExporter:
    def __init__(self, pg_config, hdfs_path, tables, hdfs_container, container_temp_dir):
        self.PG_CONFIG = pg_config
        self.HDFS_PATH = hdfs_path
        self.TABLES = tables
        self.HDFS_CONTAINER = hdfs_container
        self.CONTAINER_TEMP_DIR = container_temp_dir

    def _run_docker_command(self, cmd):
        full_cmd = f"docker exec {self.HDFS_CONTAINER} {cmd}"
        subprocess.run(full_cmd, shell=True, check=True)

    def export_tables(self):
        conn = psycopg2.connect(**self.PG_CONFIG)
        results = {}
        
        self._run_docker_command(f"mkdir -p {self.CONTAINER_TEMP_DIR}")
        
        for table in self.TABLES:
            local_csv = f"{table}.csv"
            container_csv = f"{self.CONTAINER_TEMP_DIR}/{table}.csv"
            
            try:
                print(f"Processing {table}...")
                
                # Read data from PostgreSQL
                df = pd.read_sql(f"SELECT * FROM {table}", conn)
                
                # Write to local CSV file
                df.to_csv(local_csv, index=False)
                
                # Copy CSV file to container
                copy_cmd = f"docker cp {local_csv} {self.HDFS_CONTAINER}:{container_csv}"
                subprocess.run(copy_cmd, shell=True, check=True)

                # Upload to HDFS
                self._run_docker_command(f"hdfs dfs -mkdir -p {self.HDFS_PATH}/{table}")
                self._run_docker_command(f"hdfs dfs -put -f {container_csv} {self.HDFS_PATH}/{table}/{table}.csv")
                
                # Verify file exists in HDFS
                self._run_docker_command(f"hdfs dfs -test -e {self.HDFS_PATH}/{table}/{table}.csv")
                
                results[table] = "Successfully exported to HDFS"
                print(f"✓ {table} successfully exported to HDFS")
                
            except Exception as e:
                error_msg = f"Error processing {table}: {str(e)}"
                results[table] = error_msg
                print(f"✗ {error_msg}")
            finally:
                # Clean up temporary files
                if os.path.exists(local_csv):
                    os.remove(local_csv)
                self._run_docker_command(f"rm -f {container_csv}")
        
        conn.close()
        print("All tables processed")
        return results