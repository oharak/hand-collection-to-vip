"""
Contains class that generates the 'street_segment.txt' file.

address_direction,
city,
includes_all_addresses,
includes_all_streets,
odd_even_both,
precinct_id,
start_house_number,
end_house_number,
state,
street_direction,
street_name,
street_suffix,
unit_number,
zip,
id

"""

import pandas as pd
import re
import config
import os
from tx_locality import LocalityTxt
from tx_polling_location import PollingLocationTxt
from tx_precinct import PrecinctTxt


voter_file = "C:\Users\Aaron Garris\democracyworks\hand-collection-to-vip\\texas_pp\source\\" + config.voter_file

class StreetSegmentsTxt(object):
    """Takes the merged_df passed to the class instance in main() and formats data according to VIP 5.1 specifications.

    The merged dataframe (merged_df) is referred to as the base_df within the StreetSegmentsTxt() class. The base_df
    contains the necessary data dependencies for creating street segments.

    A method is provided for each 5.1 VIP street_segment.txt column. Values are taken from one or more relevant columns
    of each row in the base dataframe (base_df) and modified as needed to create data for the new VIP columns which
    are appended to the existing base_df.

    Each method corresponding to a VIP column is called in the build method where parameters corresponding to column
    values of the same row are passed to the apply() function. Apply() is set to operate row-wise meaning a given method
    takes its input from and produces its output for the same row. In this case the values for new columns.

    In the write method the dataframe is either reindexed or the original base_df columns are dropped leaving only the
    VIP 5.1 spec columns which are then written to a text file.

    """

    def __init__(self, merged_df):
        self.base_df = merged_df

    def get_address_direction(self, vf_reg_cass_pre_directional):
        """Sets pre-directional street value taken from base_df."""
        return vf_reg_cass_pre_directional


    def get_city(self, index, vf_reg_cass_city):
        """Sets city value."""
        return vf_reg_cass_city

    def includes_all_addresses(self, vf_reg_cass_street_name, vf_reg_cass_city):
        """Not a required field and not applicable to the street_segment format."""
        return ''

    def includes_all_streets(self):
        """Not a required field and not applicable to the street_segment format."""
        return ''

    def odd_even_both(self, index, vf_reg_cass_street_num):
        """Sets the odd_even_both value. The value is always both."""
        return 'both'

    def get_precinct_id(self, van_precinctid):
        """Prepends 'pre' to precinct id value fetched from base_df."""
        return 'pre' + str(van_precinctid)

    def get_start_house_number(self, vf_reg_cass_street_num):
        """Removes invalid characters from house number and sets the start_house_number value."""

        start_house = str(vf_reg_cass_street_num)

        start_house = start_house.replace(' 1/2', '')
        start_house = start_house.replace(' 1/4', '')
        start_house = start_house.replace(' 3/4', '')
        start_house = start_house.replace('.5', '')
        start_house = start_house.replace('&', '')
        start_house = start_house.split('-')[0]
        start_house = start_house.split('/')[0]
        start_house = start_house.split(' ')[0]
        start_house = start_house.split('.')[0]

        if any(c.isalpha() for c in start_house):
            return re.sub('[^0-9]', '', start_house)
        else:
            return start_house

    def get_end_house_number(self, vf_reg_cass_street_num):
        """Removes invalid characters from house number and sets the end_house_number value."""

        end_house = str(vf_reg_cass_street_num)

        end_house = end_house.replace(' 1/2', '')
        end_house = end_house.replace(' 1/4', '')
        end_house = end_house.replace(' 3/4', '')
        end_house = end_house.replace('.5', '')
        end_house = end_house.replace('&', '')
        end_house = end_house.split('-')[0]
        end_house = end_house.split('/')[0]
        end_house = end_house.split(' ')[0]
        end_house = end_house.split('.')[0]

        if any(c.isalpha() for c in end_house):
            return re.sub('[^0-9]', '', end_house)
        else:
            return end_house

    def get_state(self, vf_reg_cass_state):
        """Sets state value."""
        return vf_reg_cass_state

    def get_street_direction(self, vf_reg_cass_pre_directional):
        """Set street direction value."""
        return vf_reg_cass_pre_directional

    def get_street_name(self, vf_reg_cass_street_name):
        """Sets street_name value."""
        return vf_reg_cass_street_name

    def get_street_suffix(self, vf_reg_cass_street_suffix):
        """Sets street_suffix value."""
        return vf_reg_cass_street_suffix

    def get_unit_number(self):
        """#"""
        return ''

    def get_zip(self, vf_reg_cass_zip):
        """Sets zip code value, adding leading zero if necessary."""
        if len(str(vf_reg_cass_zip)) == 4:
            return '0' + str(vf_reg_cass_zip)
        else:
            return vf_reg_cass_zip

    def create_id(self, index):
        """Creates a sequential id by concatenating a prefix with an 'index_str' based on the Dataframe's row index.
        Leading '0s' are added to maintain a consistent id length.
        """

        if index <=9:
            index_str = '0000' + str(index)
            return 'ss' + index_str
        elif index in range(10,100):
            index_str = '000' + str(index)
            return 'ss' + index_str
        elif index in range(100, 1000):
            index_str = '00' + str(index)
            return 'ss' + index_str
        elif index:
            index_str = str(index)
            return 'ss' + index_str

        else:
            return ''

    def build_precinct_txt(self):
        """
        New columns that match the 'street_segment.txt' template are inserted into the DataFrame, apply() is
        used to run methods that generate the values for each row of the new columns.
        """

        self.base_df['address_direction'] = self.base_df.apply(
            lambda row: self.get_address_direction(row['vf_reg_cass_pre_directional']), axis=1)

        self.base_df['city'] = self.base_df.apply(
            lambda row: self.get_city(row['index'], row['vf_reg_cass_city']), axis=1)

        self.base_df['includes_all_addresses'] = self.base_df.apply(
            lambda row: self.includes_all_addresses(row['vf_reg_cass_street_name'], row['vf_reg_cass_city']), axis=1)

        self.base_df['includes_all_streets'] = self.base_df.apply(
            lambda row: self.includes_all_streets(), axis=1)

        self.base_df['odd_even_both'] = self.base_df.apply(
            lambda row: self.odd_even_both(row['index'], row['vf_reg_cass_street_num']), axis=1)

        self.base_df['precinct_id'] = self.base_df.apply(
            lambda row: self.get_precinct_id(row['van_precinctid']), axis=1)  # could also use 'merge_key"

        self.base_df['start_house_number'] = self.base_df.apply(
            lambda row: self.get_start_house_number(row['vf_reg_cass_street_num']), axis=1)

        self.base_df['end_house_number'] = self.base_df.apply(
            lambda row: self.get_end_house_number(row['vf_reg_cass_street_num']), axis=1)

        self.base_df['state'] = self.base_df.apply(
            lambda row: self.get_state(row['vf_reg_cass_state']), axis=1)

        self.base_df['street_direction'] = self.base_df.apply(
            lambda row: self.get_street_direction(row['vf_reg_cass_pre_directional']), axis=1)

        self.base_df['street_name'] = self.base_df.apply(
            lambda row: self.get_street_name(row['vf_reg_cass_street_name']), axis=1)

        self.base_df['street_suffix'] = self.base_df.apply(
            lambda row: self.get_street_suffix(row['vf_reg_cass_street_suffix']), axis=1)

        self.base_df['unit_number'] = self.base_df.apply(
            lambda row: self.get_unit_number(), axis=1)

        self.base_df['zip'] = self.base_df.apply(
            lambda row: self.get_zip(row['vf_reg_cass_zip']), axis=1)

        self.base_df['id'] = self.base_df.apply(
            lambda row: self.create_id(row['index']), axis=1)

        return self.base_df

    def write(self):
        """Drops base DataFrame columns then writes final dataframe to text or csv file"""

        sseg = self.build_precinct_txt()
        #sseg = sseg[sseg.external_identifier_value.notnull()]

        cols = ['address_direction', 'city', 'includes_all_addresses', 'includes_all_streets', 'odd_even_both',
                'precinct_id', 'start_house_number', 'end_house_number', 'state', 'street_direction', 'street_name',
                'street_suffix', 'unit_number', 'zip', 'id']

        sseg = sseg.reindex(columns=cols)

        # Drop rows with the values: UOCAVA, CONFIDENTIAL, TEMPORARY ABSENCE
        sseg = sseg[sseg['street_name'].isin(['UOCAVA', 'CONFIDENTIAL', 'TEMPORARY ABSENCE'])== False]

        sseg.to_csv(config.output + 'street_segment.txt', index=False, encoding='utf-8')  # send to txt file
        sseg.to_csv(config.output + 'street_segment.csv', index=False, encoding='utf-8')  # send to txt file

def main():

    # subset of voter file columns
    use = ['vf_source_state', 'vf_county_name', 'vf_cd', 'vf_sd', 'vf_hd', 'vf_township', 'vf_ward', 'vf_precinct_id',
           'vf_precinct_name', 'vf_county_council', 'vf_reg_cass_address_full', 'vf_reg_cass_city', 'vf_reg_cass_state',
           'vf_reg_cass_zip', 'vf_reg_cass_zip4', 'vf_reg_cass_street_num', 'vf_reg_cass_pre_directional',
           'vf_reg_cass_street_name', 'vf_reg_cass_street_suffix', 'vf_reg_cass_post_directional', 'vf_reg_cass_unit_designator',
           'vf_reg_cass_apt_num', 'van_precinctid']

    # Create voter file dataframe.
    df = pd.read_csv(voter_file, sep=',', names=use,
                     encoding='ISO-8859-1', skiprows=1, iterator=True,
                     chunksize=1000,
                     dtype='str'
                     )

    voter_file_df = pd.concat(df, ignore_index=True)
    voter_file_df['index'] = voter_file_df.index + 1

    # create StreetSegments instance
    st = StreetSegmentsTxt(voter_file_df)
    st.write()

if __name__ == '__main__':

    main()