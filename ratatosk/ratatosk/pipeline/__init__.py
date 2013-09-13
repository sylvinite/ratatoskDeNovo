import os
import ratatosk
from ratatosk.pipeline import align, haloplex, seqcap, pippen

# Define configuration file  locations and classes for predefined workflows
config_dict = {
    'ratatosk' : {'config':os.path.join(ratatosk.__path__[0], os.pardir, "config", "ratatosk.yaml"),
                  'cls':None},
    'Align' : {'config' : os.path.join(ratatosk.__path__[0], os.pardir, "config", "align.yaml"),
               'cls' : align.Align},
    'HaloPlex' : {'config' : os.path.join(ratatosk.__path__[0], os.pardir, "config", "haloplex.yaml"),
               'cls' : haloplex.HaloPlex},
    'HaloPlexSummary' : {'config' : os.path.join(ratatosk.__path__[0], os.pardir, "config", "haloplex.yaml"),
               'cls' : haloplex.HaloPlexSummary},
    'HaloPlexCombine' : {'config' : os.path.join(ratatosk.__path__[0], os.pardir, "config", "haloplex.yaml"),
               'cls' : haloplex.HaloPlexCombine},

    'Pippen': {'config' : os.path.join(ratatosk.__path__[0], os.pardir, "config", "pippen.yaml"),
		'cls' : pippen.Pippen},
    'Seqcap' : {'config' : os.path.join(ratatosk.__path__[0], os.pardir, "config", "seqcap.yaml"),
                'cls' : seqcap.SeqCap},
    'SeqcapSummary' : {'config' : os.path.join(ratatosk.__path__[0], os.pardir, "config", "seqcap.yaml"),
                       'cls' : seqcap.SeqCapSummary},
    }
