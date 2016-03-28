import tarfile
import os
import sys
    
def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
        

if __name__ == "__main__":
   make_tarfile(sys.argv[1],sys.argv[2])
