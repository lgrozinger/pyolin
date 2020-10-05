import sbol
import zipfile
import pathlib
import re


def fixseva221accession(path):
    match = r'LOCUS\s+(\S+)(.*)'
    replace = r'LOCUS       JX560327    \2'
    with open('/tmp/tmpgenbank.gbk', 'w') as tmp:
        with open(path) as old:
            for line in old:
                tmp.write(re.sub(match, replace, line, count=1))

    with open('/tmp/tmpgenbank.gbk') as tmp:
        with open(path, 'w') as old:
            old.write(tmp.read())
    

if __name__ == '__main__':
    with zipfile.ZipFile('./genbank.zip', 'r') as zipped:
        zipped.extractall()

        for path in pathlib.Path('.').glob('**/**/*.gbk'):
            sboldoc = sbol.Document()
            print(f"CONVERTING: {path}")
            if 'pSeva221' in str(path):
                fixseva221accession(path)

            try:
                sboldoc.importFromFormat('GenBank', str(path))
                sboldoc.write(f"{path.stem}.xml")
            except ValueError:
                print(f"GENBANK CONVERSION FAIL: {path}")

    with zipfile.ZipFile('./fasta.zip', 'r') as zipped:
        zipped.extractall()

        for path in pathlib.Path('.').glob('**/**/*.fa'):
            sboldoc = sbol.Document()
            print(f"CONVERTING: {path}")
            try:
                sboldoc.importFromFormat('FASTA', str(path))
                sboldoc.write(f"{path.stem}.xml")
            except ValueError:
                print(f"FASTA CONVERSION FAIL: {path}")


    
