import pandas as pd
import re
import config





class LocalityTxt(object):
    """#
    """

    def __init__(self, early_voting_df, state):
        self.base_df = early_voting_df
        self.state = state

    def create_election_administration_id(self, index):
        """Creates election_administration_ids by concatenating a prefix with an 'index_str' based on the Dataframe's
        row index. '0s' are added, if necesary, to maintain a consistent id length. As currently designed the method
        works up to index 9,999"""
        return ''
        # prefix = 'ea'
        #
        # if index <= 9:
        #     index_str = '000' + str(index)
        #     return prefix + index_str
        #
        # elif index in range(10,100):
        #     index_str = '00' + str(index)
        #     return prefix + index_str
        #
        # elif index >= 100:
        #     index_str = '0' + str(index)
        #     return prefix + index_str
        #
        # else:
        #     index_str = str(index)
        #     return prefix + index_str

    def get_external_identifier_type(self):
        """#"""
        return "ocd-id"

    def get_external_identifier_othertype(self):
        # create conditional when/if column is present
        return ''

    def get_external_identifier_value(self, external_identifier_value):
        """Extracts external identifier (ocd-division)."""
        county = external_identifier_value.split(" ")
        county = county[len(county)-1]
        if external_identifier_value:
            str = "ocd-division/country:us/state:" + config.state_lower_abbreviation + "/county:" + county.lower()
            return str
            # ocd-division/country:us/state:nj/county:atlantic
        else:
            return ''

    def create_name(self, index, division_description ):
        """
        Creates a name by concatenating the 'locality' (town name along with town or county designation)
        with an 'index_str' based on the Dataframes row index.'0s' are added, if necesary, to
        maintain a consistent id length.
        """

        # Get locality(town or county), and remove state abbreviation.
        if division_description:
            locality = division_description[:-3].lower().replace(" ", "_")
            #print locality
        else:
            locality = ''
            print 'Missing data at row ' + str(index) + '.'

        # Add leading '0s' depending on index number.
        if index <= 9:
            index_str = '000' + str(index)

        elif index in range(10,100):
            index_str = '00' + str(index)

        elif index >= 100:
            index_str = '0' + str(index)
        else:
            index_str = str(index)

        return locality + index_str

    def create_polling_location_ids(self, polling_location_id):
        """
        Creates polling_location_ids by concatenating 'poll' with an 'index_str' based on the Dataframe's row index.
        '0s' are added, if necesary, to maintain a consistent id length.
        """

        return polling_location_id

    def create_state_id(self):
        """Creates the state_id by matching a key in the state_dict and retrieving
        and modifying its value. A '0' is added, if necessary, to maintain a
        consistent id length.
        """
        for key, value in config.fips_dict.iteritems():
            if key == self.state.lower():
                state_num = value
                if state_num <=9:
                    state_num = '0' + str(state_num)
                else:
                    state_num = str(state_num)

                return 'st' + state_num

    def get_type(self):
        # create conditional when/if column is present
        return ''

    def get_other_type(self):
        # create conditional when/if column is present
        return 'other'


    def create_id(self, index):
        """Creates a sequential id by concatenating 'loc' with an 'index_str' based on the Dataframe's row index.
        '0s' are added, if necesary, to maintain a consistent id length.
        """

        if index <=9:
            index_str = '000' + str(index)
            return 'loc' + index_str

        elif index in range(10,100):
            index_str = '00' + str(index)
            return 'loc' + index_str

        elif index >= 100:
            index_str = '0' + str(index)
            return 'loc' + index_str

        elif index:
            index_str = str(index)
            return 'loc' + index_str

        else:
            return ''

    def build_locality_txt(self):
        """
        New columns that match the 'locality.txt' template are inserted into the DataFrame, apply() is
        used to run methods that generate the values for each row of the new columns.
        """
        self.base_df['election_administration_id'] = self.base_df.apply(
            lambda row: self.create_election_administration_id(row['index']), axis=1)

        self.base_df['external_identifier_type'] = self.base_df.apply(
            lambda row: self.get_external_identifier_type(), axis=1)

        self.base_df['external_identifier_othertype'] = self.base_df.apply(
            lambda row: self.get_external_identifier_othertype(), axis=1)

        self.base_df['external_identifier_value'] = self.base_df.apply(
            lambda row: self.get_external_identifier_value(row['county']), axis=1)

        self.base_df['name'] = self.base_df.apply(
            lambda row: self.create_name(row['index'], row['county']), axis=1)

        self.base_df['polling_location_ids'] = self.base_df.apply(
            lambda row: self.create_polling_location_ids(row['polling_location_id']), axis=1)

        self.base_df['state_id'] = self.base_df.apply(
            lambda row: self.create_state_id(), axis=1)

        self.base_df['type'] = self.base_df.apply(
            lambda row: self.get_type(), axis=1)

        self.base_df['other_type'] = self.base_df.apply(
            lambda row: self.get_other_type(), axis=1)

        self.base_df['id'] = self.base_df.apply(
            lambda row: self.create_id(row['index']), axis=1)

        return self.base_df

    def write_locality_txt(self):
        """Drops base DataFrame columns then writes final dataframe to text or csv file"""

        loc = self.build_locality_txt()
        #print loc

        # Drop base_df columns.
        loc.drop(['county', 'address', 'instructions', 'start_time', 'end_time', 'start_date', 'count', 'end_date', 'address_line', 'directions',
                'hours', 'photo_uri', 'hours_open_id', 'is_drop_box', 'is_early_voting', 'lat',
                  'long', 'latlng', 'polling_location_id', 'index'], inplace=True, axis=1)

        print loc

        txt_file = "/Users/danielgilberg/Development/hand-collection-to-vip/hawaii/output/locality.txt"
        csv_file = "/Users/danielgilberg/Development/hand-collection-to-vip/hawaii/output/locality.csv"

        loc.to_csv(csv_file, index=False, encoding='utf-8')  # send to txt file
        loc.to_csv(txt_file, index=False, encoding='utf-8')  # send to csv file

    def final_build(self):
        loc = self.build_locality_txt()
        # print loc

        loc = loc.groupby(['hours_open_id']).agg(lambda x: ' '.join(set(x))).reset_index()
        # print loc

        loc['name'] = loc['name'].apply(lambda x: ''.join(x.split(' ')[0]))

        loc['grouped_index'] = loc.index + 1
        print type(loc['grouped_index'])

        loc['id'] = loc.apply(
            lambda row: self.create_id(row['grouped_index']), axis=1)
        # print loc

        print loc['id']

        # reorder columns
        cols = ['election_administration_id', 'external_identifier_type', 'external_identifier_othertype',
                'external_identifier_value', 'name', 'polling_location_ids', 'state_id', 'type',
                'other_type', 'grouped_index', 'id']

        final = loc.reindex(columns=cols)
        # print final

        final.drop(['grouped_index'], inplace=True, axis=1)
        print final

        # final.drop(['grouped_index',  'address_line', 'hours', 'photo_uri', 'hours_open_id',
        #            'is_drop_box', 'is_early_voting', 'latitude', 'longitude', 'latlng_source',
        #          'polling_location_id'], inplace=True, axis=1)
        txt_file = "/Users/danielgilberg/Development/hand-collection-to-vip/hawaii/output/locality.txt"
        csv_file = "/Users/danielgilberg/Development/hand-collection-to-vip/hawaii/output/locality.csv"

        final.to_csv(csv_file, index=False, encoding='utf-8')  # send to txt file
        final.to_csv(txt_file, index=False, encoding='utf-8')  # send to csv file
        return final


if __name__ == '__main__':
    state_file = 'intermediate_doc.csv'

    early_voting_file = config.output + state_file

    colnames = ['county', 'loc_name', 'address', 'instructions', 'start_time', 'end_time', 'start_date', 'count', 'end_date',
                'index', 'name', 'address_line', 'directions',
                'hours', 'photo_uri', 'hours_open_id', 'is_drop_box', 'is_early_voting', 'lat', 'long', 'latlng', 'polling_location_id']
    print len(colnames)
    early_voting_df = pd.read_csv(early_voting_file, names=colnames, encoding='utf-8', skiprows=1)

    early_voting_df['index'] = early_voting_df.index +1 # offsets zero based index so it starts at 1 for ids


    lt = LocalityTxt(early_voting_df, "Hawaii")
    lt.final_build()