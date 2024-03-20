import requests

host = 'http://pantherdb.org'
gene_mapping_api = '/services/oai/pantherdb/geneinfo'
params = {"geneInputList":"ABCA1", "organism":9606}

def load_chromosomal_location(dfile='./data/others/Homo_sapiens.chromosome_location_hg19'):
    dic = {}
    for i in open(dfile):
        line = i.rstrip().split('\t')
        dic[line[0]] = (line[1], int(line[2]), int(line[3]))
    return dic
    
def map_gene(k):
    params["geneInputList"] = k
    try:
        r = requests.get(url = host + gene_mapping_api, params = params, timeout=5)
        data = r.json()
        return data['search']['mapped_genes']['gene']["accession"]
    except:
        print('gene mapping error:', k)
        return ''

def get_pos_from_gene_id(gid, chromosomal_location_dic):
    return chromosomal_location_dic.get(gid ,None)

chromosomal_location_dic = load_chromosomal_location('./data/others/Homo_sapiens.chromosome_location_hg19')


