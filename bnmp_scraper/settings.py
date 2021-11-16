__version__ = "0.0.1"

UF_MAP = {'AC': 1, 'AL': 2, 'AM': 3, 'AP': 4, 'BA': 5, 'CE': 6, 'DF': 7, 'ES': 8, 'GO': 9, 'MA': 10, 'MG': 11, 'MS': 12,
          'MT': 13, 'PA': 14, 'PB': 15, 'PE': 16, 'PI': 17, 'PR': 18, 'RJ': 19, 'RN': 20, 'RO': 21, 'RR': 22, 'RS': 23,
          'SC': 24, 'SE': 25, 'SP': 26, 'TO': 27}

NUM_MAP = {1: 'AC', 2: 'AL', 3: 'AM', 4: 'AP', 5: 'BA', 6: 'CE', 7: 'DF', 8: 'ES', 9: 'GO', 10: 'MA', 11: 'MG',
           12: 'MS', 13: 'MT', 14: 'PA', 15: 'PB', 16: 'PE', 17: 'PI', 18: 'PR', 19: 'RJ', 20: 'RN', 21: 'RO', 22: 'RR',
           23: 'RS', 24: 'SC', 25: 'SE', 26: 'SP', 27: 'TO'}

PARAMS_FORCA_BRUTA = [(('page', '0'), ('size', '2000'), ('sort', 'numeroPeca,ASC')),
                      (('page', '0'), ('size', '2000'), ('sort', 'numeroPeca,DESC')),
                      (('page', '0'), ('size', '2000'), ('sort', 'nomePessoa,ASC')),
                      (('page', '0'), ('size', '2000'), ('sort', 'nomePessoa,DESC')),
                      (('page', '0'), ('size', '2000'), ('sort', 'descricaoStatus,ASC')),
                      (('page', '0'), ('size', '2000'), ('sort', 'descricaoStatus,DESC')),
                      (('page', '0'), ('size', '2000'), ('sort', 'dataExpedicao,ASC')),
                      (('page', '0'), ('size', '2000'), ('sort', 'dataExpedicao,DESC')),
                      (('page', '0'), ('size', '2000'), ('sort', 'descricaoPeca,ASC')),
                      (('page', '0'), ('size', '2000'), ('sort', 'descricaoPeca,DESC')),
                      (('page', '1'), ('size', '2000'), ('sort', 'numeroPeca,ASC')),
                      (('page', '1'), ('size', '2000'), ('sort', 'numeroPeca,DESC')),
                      (('page', '1'), ('size', '2000'), ('sort', 'nomePessoa,ASC')),
                      (('page', '1'), ('size', '2000'), ('sort', 'nomePessoa,DESC')),
                      (('page', '1'), ('size', '2000'), ('sort', 'descricaoStatus,ASC')),
                      (('page', '1'), ('size', '2000'), ('sort', 'descricaoStatus,DESC')),
                      (('page', '1'), ('size', '2000'), ('sort', 'dataExpedicao,ASC')),
                      (('page', '1'), ('size', '2000'), ('sort', 'dataExpedicao,DESC')),
                      (('page', '1'), ('size', '2000'), ('sort', 'descricaoPeca,ASC')),
                      (('page', '1'), ('size', '2000'), ('sort', 'descricaoPeca,DESC')),
                      (('page', '2'), ('size', '2000'), ('sort', 'numeroPeca,ASC')),
                      (('page', '2'), ('size', '2000'), ('sort', 'numeroPeca,DESC')),
                      (('page', '2'), ('size', '2000'), ('sort', 'nomePessoa,ASC')),
                      (('page', '2'), ('size', '2000'), ('sort', 'nomePessoa,DESC')),
                      (('page', '2'), ('size', '2000'), ('sort', 'descricaoStatus,ASC')),
                      (('page', '2'), ('size', '2000'), ('sort', 'descricaoStatus,DESC')),
                      (('page', '2'), ('size', '2000'), ('sort', 'dataExpedicao,ASC')),
                      (('page', '2'), ('size', '2000'), ('sort', 'dataExpedicao,DESC')),
                      (('page', '2'), ('size', '2000'), ('sort', 'descricaoPeca,ASC')),
                      (('page', '2'), ('size', '2000'), ('sort', 'descricaoPeca,DESC')),
                      (('page', '3'), ('size', '2000'), ('sort', 'numeroPeca,ASC')),
                      (('page', '3'), ('size', '2000'), ('sort', 'numeroPeca,DESC')),
                      (('page', '3'), ('size', '2000'), ('sort', 'nomePessoa,ASC')),
                      (('page', '3'), ('size', '2000'), ('sort', 'nomePessoa,DESC')),
                      (('page', '3'), ('size', '2000'), ('sort', 'descricaoStatus,ASC')),
                      (('page', '3'), ('size', '2000'), ('sort', 'descricaoStatus,DESC')),
                      (('page', '3'), ('size', '2000'), ('sort', 'dataExpedicao,ASC')),
                      (('page', '3'), ('size', '2000'), ('sort', 'dataExpedicao,DESC')),
                      (('page', '3'), ('size', '2000'), ('sort', 'descricaoPeca,ASC')),
                      (('page', '3'), ('size', '2000'), ('sort', 'descricaoPeca,DESC')),
                      (('page', '4'), ('size', '2000'), ('sort', 'numeroPeca,ASC')),
                      (('page', '4'), ('size', '2000'), ('sort', 'numeroPeca,DESC')),
                      (('page', '4'), ('size', '2000'), ('sort', 'nomePessoa,ASC')),
                      (('page', '4'), ('size', '2000'), ('sort', 'nomePessoa,DESC')),
                      (('page', '4'), ('size', '2000'), ('sort', 'descricaoStatus,ASC')),
                      (('page', '4'), ('size', '2000'), ('sort', 'descricaoStatus,DESC')),
                      (('page', '4'), ('size', '2000'), ('sort', 'dataExpedicao,ASC')),
                      (('page', '4'), ('size', '2000'), ('sort', 'dataExpedicao,DESC')),
                      (('page', '4'), ('size', '2000'), ('sort', 'descricaoPeca,ASC')),
                      (('page', '4'), ('size', '2000'), ('sort', 'descricaoPeca,DESC')),
                      (('page', '0'), ('size', '2000'), ('sort', '')),
                      (('page', '1'), ('size', '2000'), ('sort', '')),
                      (('page', '2'), ('size', '2000'), ('sort', '')),
                      (('page', '3'), ('size', '2000'), ('sort', '')),
                      (('page', '4'), ('size', '2000'), ('sort', ''))]