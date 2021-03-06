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
from nh_locality import LocalityTxt
from nh_polling_location import PollingLocationTxt
from nh_precinct import PrecinctTxt

f = 'tsmart_google_geo_20160817_NH_20160520.txt'

voter_file = "C:\Users\Aaron Garris\democracyworks\hand-collection-to-vip\\new_hampshire_pp\source\\" + f

class StreetSegmentsTxt(object):
    """#"""

    def __init__(self, merged_df):
        self.base_df = merged_df
        #print self.base_df

    def get_address_direction(self, vf_reg_cass_pre_directional):
        """#"""
        return vf_reg_cass_pre_directional


    def get_city(self, index, vf_reg_cass_city):
        """#"""
        print 'Processing' + str(vf_reg_cass_city)
        #print index, vf_reg_cass_city
        return vf_reg_cass_city

    def includes_all_addresses(self, vf_reg_cass_street_name, vf_reg_cass_city):
        """#"""
        return ''
        # TODO: for includes_all_addresses - groupby street and city. if set(precinct_ids) >=2: includes_all... = false
#        precinct_ids = []
#        a = self.base_df[(self.base_df['vf_reg_cass_street_name'] == vf_reg_cass_street_name) & (self.base_df['vf_reg_cass_city'] == vf_reg_cass_city)]
        #b = a.count()
#        b = a.shape
        #print b
        #print vf_reg_cass_street_name + ',', vf_reg_cass_city_y + ',' + 'Count is ' + str(b)

#        if b.count == 1:
            #print 'true'
#            return 'true'
#        else:
            #print 'false'
#            return 'false'

    def includes_all_streets(self):
        """#"""
        return ''

    def odd_even_both(self, index, vf_reg_cass_street_num):
        """#"""
        return 'both'

#        if len(vf_reg_cass_street_num) >=1:

#            oel = vf_reg_cass_street_num.split(',')  # create list of strings from grouped street number string

#            oel = [x for x in oel if any(c.isdigit() for c in x)]  # keep any strings containing numbers

#            clean_oel = [re.sub('[^0-9]', '', x) for x in oel]  # remove any non numeric values from strings

#            odd_even_list = set(["even" if int(i) % 2 == 0 else "odd" for i in clean_oel])
            #print odd_even_list

#            print odd_even_list
            # if dealing with floats instead of integers
            #odd_even_list = set(["even" if int(i * 10) % 2 == 0 else "odd" for i in vf_reg_cass_street_num.split(' ')])

#            if 'even' in odd_even_list and 'odd' in odd_even_list:
#                return 'both'

#            elif len(odd_even_list) == 1 and 'even' in odd_even_list:
#                return 'even'

#            elif len(odd_even_list) == 1 and 'odd' in odd_even_list:
#                return 'odd'
#            else:
#                print 'Non-numeric or missing street number value at row' + ' ' + str(index) + '.'
            #raise ValueError()
#        else:
#            raise ValueError()


    def get_precinct_id(self, van_precinctid):
        """#"""
        return 'pre' + str(van_precinctid)

    def get_start_house_number(self, vf_reg_cass_street_num):
        """#"""

        start_house = str(vf_reg_cass_street_num)
        #remove = ['1/2', '1/2 1/2', '3/4', '1/4' '.5']
        #start_house = start_house.translate(None, ''.join(remove))
        start_house = start_house.replace(' 1/2', '')
        start_house = start_house.replace(' 1/4', '')
        start_house = start_house.replace(' 3/4', '')
        start_house = start_house.replace('.5', '')
        start_house = start_house.split('-')[0]
        start_house = start_house.split('/')[0]

        if any(c.isalpha() for c in start_house):
            return re.sub('[^0-9]', '', start_house)
        else:
            return start_house

#        start_house_list = vf_reg_cass_street_num.split(',')

#        print vf_reg_cass_street_num

#        start_house_list = [x for x in start_house_list if any(c.isdigit() for c in x)]  # keep any strings containing numbers

#        clean_start_house_list = [re.sub('[^0-9]', '', x) for x in start_house_list]  # remove any non numeric values from strings

#        print clean_start_house_list
        # re.sub('[^0-9]', '', a)
#        if len(clean_start_house_list) == 1:
#            return clean_start_house_list[0]
#        else:

#            try:

                #start_house = [int(i) for i in vf_reg_cass_street_num.split(',')]
#                start_house = str(min([int(i) for i in clean_start_house_list]))

#                return start_house
#            except:
#                pass

    def get_end_house_number(self, vf_reg_cass_street_num):
        """#"""
        #return vf_reg_cass_street_num
        end_house = str(vf_reg_cass_street_num)
        end_house = end_house.replace(' 1/2', '')
        end_house = end_house.replace(' 1/4', '')
        end_house = end_house.replace(' 3/4', '')
        end_house = end_house.replace('.5', '')
        end_house = end_house.split('-')[0]
        end_house = end_house.split('/')[0]

        if any(c.isalpha() for c in end_house):
            return re.sub('[^0-9]', '', end_house)
        else:
            return end_house

        # TODO: no need to handle fractions, just get the first element, they're already ordered, add conditional, raise valueerror
        #return min([int(i) for i in vf_reg_cass_street_num.split(' ')])
#        print vf_reg_cass_street_num

#        end_house_list = [x for x in end_house_list if any(c.isdigit() for c in x)]  # keep any strings containing numbers

#        clean_end_house_list = [re.sub('[^0-9]', '', x) for x in end_house_list]  # remove any non numeric values from strings
#        return clean_end_house_list

        #print clean_end_house_list
#        if len(clean_end_house_list) ==1:
#            return clean_end_house_list[0]
#        else:

#            try:

#                end_house = str(max([int(i) for i in clean_end_house_list]))

#                return end_house
#            except:
#                pass

    def get_state(self, vf_reg_cass_state):
        """#"""
        return vf_reg_cass_state

    def get_street_direction(self, vf_reg_cass_pre_directional):
        """#"""
        return vf_reg_cass_pre_directional

    def get_street_name(self, vf_reg_cass_street_name):
        print 'Processing' + str(vf_reg_cass_street_name)
        return vf_reg_cass_street_name

    def get_street_suffix(self, vf_reg_cass_street_suffix):
        """#"""
        return vf_reg_cass_street_suffix

    def get_unit_number(self):
        """#"""
        return ''

    def get_zip(self, vf_reg_cass_zip):
        """#"""
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

    def counter(self):
        """#"""
        pass

    def write(self):
        """Drops base DataFrame columns then writes final dataframe to text or csv file"""

        sseg = self.build_precinct_txt()
        sseg = sseg[sseg.external_identifier_value.notnull()]


        cols = ['address_direction', 'city', 'includes_all_addresses', 'includes_all_streets', 'odd_even_both',
                'precinct_id', 'start_house_number', 'end_house_number', 'state', 'street_direction', 'street_name',
                'street_suffix', 'unit_number', 'zip', 'id']

        sseg = sseg.reindex(columns=cols)


        sseg = sseg.drop_duplicates(subset=['address_direction', 'city', 'includes_all_addresses', 'includes_all_streets',
                                            'odd_even_both', 'precinct_id', 'start_house_number', 'end_house_number',
                                            'street_direction', 'street_name', 'street_suffix', 'unit_number', 'zip'])

        # Drop rows with the values: UOCAVA, CONFIDENTIAL, TEMPORARY ABSENCE
        sseg = sseg[sseg['street_name'].isin(['UOCAVA', 'CONFIDENTIAL', 'TEMPORARY ABSENCE'])== False]

        sseg.to_csv(config.output + 'street_segment.txt', index=False, encoding='utf-8')  # write to txt file


def main():
    """Creates voter file dataframe and passes it to an instance of StreetSegmentsTxt()."""

    use = ['vf_source_state', 'vf_county_code', 'vf_county_name', 'vf_cd', 'vf_sd', 'vf_hd', 'vf_township', 'vf_ward',
                'vf_precinct_id', 'vf_precinct_name', 'vf_county_council', 'vf_reg_cass_address_full', 'vf_reg_cass_city',
                'vf_reg_cass_state', 'vf_reg_cass_zip', 'vf_reg_cass_zip4', 'vf_reg_cass_street_num', 'vf_reg_cass_pre_directional',
                'vf_reg_cass_street_name', 'vf_reg_cass_street_suffix', 'vf_reg_cass_post_directional', 'vf_reg_cass_unit_designator',
                'vf_reg_cass_apt_num', 'van_precinctid']

    # state voter file import
    df = pd.read_csv(voter_file, sep='\t', names=config.voter_file_columns, usecols=use,
                                 encoding='ISO-8859-1', skiprows=1, iterator=True,
                                 chunksize=1000,
                                 dtype='str',
                                )

    voter_file_df = pd.concat(df, ignore_index=True)
    voter_file_df['index'] = voter_file_df.index + 1

    st = StreetSegmentsTxt(voter_file_df)
    st.write()

if __name__ == '__main__':

    main()