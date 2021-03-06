# sudo apt-get install python3-pip
# sudo python3 -m pip install pip --upgrade
# sudo pip install pandas
# sudo python3 -m pip install py2neo
# wget https://www.dropbox.com/s/z53qgw23lw042ij/BF201808.csv
import pandas as pd
from py2neo import *
import sys


class BolsaFamilia:
	GRAPH = Graph()

	def cleanDatabase(self):
		self.GRAPH.run("MATCH (n) DETACH DELETE n;")

	def loadDatabase(self):
		files = [f for f in os.listdir("/home/pibiti_marcos/DownloadDados") if f.startswith('201') and f.endswith('.csv')]
        #print(files)
        for filename in files:
                for dataframe in pd.read_csv(filename, sep=";", chunksize=10 ** 6):
			for index, linha in dataframe.iterrows():
				sys.stdout.write('.')
				tx = self.GRAPH.begin()
				p = Node("Pagamento", 
					mesReferencia=linha['MÊS REFERÊNCIA'],
					mesCompetencia=linha['MÊS COMPETÊNCIA'], 
					nomeMunicipio=linha['NOME MUNICÍPIO'], 
					valorParcela=linha['VALOR PARCELA'],
					codigoMunicipio=linha['CÓDIGO MUNICÍPIO SIAFI'],
					uf=linha['UF']
					)
				b = Node("Beneficiario", 
					nome=linha['NOME FAVORECIDO'], 
					nis=linha['NIS FAVORECIDO']
				)
				tx.create(p)
				tx.merge(b, "Beneficiario", "nis")
				b_p = Relationship(b, "RECEBEU", p)
				tx.create(b_p)
				tx.commit()

bf = BolsaFamilia()
bf.cleanDatabase()
bf.loadDatabase()
