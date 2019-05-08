#!/usr/bin/env python3
"""
Author : kai
Date   : 2019-04-21
Purpose: Print nutrient profiles from the Amazon Continuum Metagenomes
"""

import argparse
import sys
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pandas as pd

# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Argparse Python script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'xml', metavar='XML', help='XML input')


    return parser.parse_args()


# --------------------------------------------------
def warn(msg):
    """Print a message to STDERR"""
    print(msg, file=sys.stderr)


# --------------------------------------------------
def die(msg='Something bad happened'):
    """warn() and exit with error"""
    warn(msg)
    sys.exit(1)


# --------------------------------------------------
def main():
    """Make a jazz noise here"""
    args = get_args()
    in_file = args.xml

    if not os.path.isfile(in_file):
        print('input file "{}" is not a file'.format(in_file), file=sys.stderr)
        sys.exit(1)

    tree = ET.parse(in_file)
    root = tree.getroot()
    data_list = []

    # parse the xml file and make a list of dictionaries containing all the metadata
    for elem in root:
        d = {}
        for ids in elem.findall('Ids'):
            for sub_ids in ids:
                #d[sub_ids.attrib['db']] = sub_ids.text
                for key, val in sub_ids.attrib.items():
                    #print(key, val)
                    d[val] = sub_ids.text

        for att in elem.findall('Attributes'):
            #print(att.tag, att.attrib)
            for sub_att in att:
                #print(sub_att.attrib, sub_att.text)
                d[sub_att.attrib['attribute_name']] = sub_att.text
        data_list.append(d)


    #print(len(data_list))

    # for x in data_list:
    #     print(x)

    #example data dictionary
    '''
    {'BioSample': 'SAMN02628401', '1': 'SAMN02628401', 'Sample name': 'ACM1', 'SRA': 'SRS565747',
     'env_package': 'MIGS/MIMS/MIMARKS.water', 'investigation_type': 'Metagenome',
     'sampling_cruise': 'R/V Knorr, May-June 2010', 'target_molecules': 'Genomic DNA',
     'biome': 'surface seawater', 'feature': 'Amazon River Plume',
     'geo_loc_name': 'Atlantic Ocean:Western Tropical North Atlantic Ocean',
     'site_name': 'Station 2', 'lat_lon': '10.29 -54.51', 'collection_date': '2010-05-25',
     'collection_time': '0755', 'depth': '4.47 m', 'material': 'water', 'samp_volume': '10.8 L',
     'min_filter_size': '2.0 _m', 'max_filter_size': '156 _m', 'temp': '28.63 C',
     'salinity': '31.80 PSU', 'pressure': '4.50 Db', 'density': '1019.80 kgm-2',
     'sigma-theta': '19.78', 'diss_oxy': '196.25 _mol/kg', 'oxy_sat': '98.70 pct',
     'beam_trans': '90.13 pct', 'beam_atten': '0.42 m-1', 'fluorescence': '0.61 mgm-3',
     'turbidity': '1.17 NTU', 'surf_irradiance': '796.66 _Em-2sec-1', 'corr_irradiance': '2.09 pct',
     'PAR': '16.71 _Em-2sec-1', 'bacteria_carb_prod': '112.48 pmol leu/L/hr',
     'diss_inorg_carb': '1802 _mol/kg', 'sequencing_method': 'Illumina PE 150x150',
     'sequencing_machine': 'Genome Analyzer IIx', 'std_norm_factor': '326737'}
    '''


    '''
    {'BioSample': 'SAMN05944599', '1': 'SAMN05944599', 'Sample name': 'ACJ48', 'SRA': 'SRS1776191',
    'sampling_cruise': 'R/V Atlantis, July 2012', 'investigation_type': 'metagenome',
    'target_molecules': 'Genomic DNA', 'env_biome': 'surface seawater', 'env_feature': 'Amazon River Plume',
    'isolation_source': 'water', 'geo_loc_name': 'Atlantic Ocean:Western Tropical North Atlantic Ocean',
    'site_name': 'Station 6', 'lat_lon': '3.506 N 50.500 W', 'collection_date': '2012-07-21',
    'collection_time': '9:41', 'depth': '2 m', 'samp_volume': '5', 'min_filter_size': '2.0 µm',
    'max_filter_size': '156 µm', 'temp': '27.96 C', 'salinity': '31.91 PSU', 'pressure': '1.2 Db',
     'density': '1.0201 g/ml', 'sigma-theta': '20.09', 'diss_oxy': '239.1 µmol/kg', 'oxy_sat': '115.7 pct',
     'beam_trans': '5.3 pct', 'beam_atten': '11.75 m-1', 'fluorescence': '0.47 mgm-3', 'turbidity': '-999',
     'surf_irradiance': '1399 µEm-2sec-1', 'corr_irradiance': '1 pct', 'PAR': '0.0260 µEm-2sec-1',
     'bacteria_carb_prod': '1079 pmol leu/L/hr', 'diss_inorg_carb': '1644 µmol/kg',
     'sequencing_method': 'Illumina SE 250 Rapid Run', 'sequencing_machine': 'HiSeq 2500', 'std_norm_factor': '153763.4'}
    '''


    # y=0
    #
    # for x in data_list:
    #     #print(x)
    #     #if x
    #     #print(x['investigation_type'])
    #     if 'diss_oxy' in x:
    #         #print(x)
    #         y +=1
    #         print(x)
    #
    # print(y)

    #data = [{'a': 1, 'b': 2},{'a': 5, 'b': 10, 'c': 20}]
    df = pd.DataFrame(data_list)
    #print(df)


    df.to_csv('amazon_cont_all.tsv', sep='\t', encoding='utf-8')




    # ### extract depth vs dissolved Oxygen
    # depth1 = []
    # diss_oxy = []
    # for x in data_list:
    #     if 'diss_oxy' in x and 'depth' in x:
    #         depth1.append(float(x['depth'].split()[0]))
    #         diss_oxy.append(float(x['diss_oxy'].split()[0]))
    #
    #         depth_unit = x['depth'].split()[1]
    #         diss_oxy_unit = x['diss_oxy'].split()[1]
    #
    # #plot the dissolved Oxygen profile
    # plt.plot(diss_oxy, depth1, 'ro')
    # plt.title('Dissolved Oxygen vs Depth')
    # plt.xlabel(diss_oxy_unit)
    # plt.ylabel(depth_unit)
    # #plt.show()
    # plt.savefig('Dissolved_Oxygen_profile.png')
    #
    # print('see Dissolved_Oxygen_profile.png')
    #
    # ### extract depth vs dissolved inorganic carbon
    # depth2 = []
    # diss_inorg_carb = []
    # for x in data_list:
    #     if 'diss_inorg_carb' in x and 'depth' in x:
    #         depth2.append(float(x['depth'].split()[0]))
    #         diss_inorg_carb.append(float(x['diss_inorg_carb'].split()[0]))
    #
    #         #depth_unit = x['depth'].split()[1]
    #         diss_inorg_carb_unit = x['diss_inorg_carb'].split()[1]
    #
    # #plot dissolved inorganic carbon profile
    # plt.clf()
    # plt.plot(diss_inorg_carb, depth2, 'ro')
    # plt.title('Dissolved Inorganic Carbon vs Depth')
    # plt.xlabel(diss_inorg_carb_unit)
    # plt.ylabel(depth_unit)
    # plt.tick_params(axis='x', labelsize=5)
    # #plt.show()
    # plt.savefig('Dissolved_Inorganic_carbon_profile.png')
    #
    # print('see Dissolved_Inorganic_carbon_profile.png')

# --------------------------------------------------
if __name__ == '__main__':
    main()
