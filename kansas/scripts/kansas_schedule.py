"""
start_time,
end_time,
is_only_by_appointment,
is_or_by_appointment,
is_subject_to_change,
start_date,
end_date,
hours_open_id,
id
"""

import pandas as pd
import config
from kansas_polling_location import PollingLocationTxt
import datetime


class ScheduleTxt(object):

    def __init__(self, base_df, early_voting_true='false', drop_box_true='false'):
        self.base_df = base_df

    def format_for_schedule(self):

        sch_base_df = self.base_df

        # Drop base_df columns.
        sch_base_df.drop(['index', 'county', 'officer', 'email', 'blank', 'phone', 'fax', 'address_one',
                          'address_two', 'city', 'state', 'zip', 'times', 'start_date', 'end_date', 'time_zone'],
                         inplace=True, axis=1)

        # print self.dedupe(sch_base_df)

        print sch_base_df

        # return self.dedupe(sch_base_df)


    def utc_offset(self, county):
        counties = ["Greeley", "Hamilton", "Sherman", "Wallace"]
        if county in counties:
            return "-7:00"
        else:
            return "-6:00"

    def get_sch_start_time(self, hours, county):
        offset = self.utc_offset(county)
        hour = hours.split("-")[0]
        return hour + ":00" + offset
        # arr = hours.split("-")
        # offset = self.utc_offset(county)
        # print arr[0] + ";00" + offset

    def get_sch_end_time(self, hours, county):
        offset = self.utc_offset(county)
        hours = hours.split(" ")[0]
        hour = hours.split("-")[1]
        return hour + ":00" + offset

    # def get_sch_start_time(self, start_time):
    #     # return self.convert_to_uct()
    #     start_time = tuple(start_time.split('-'))[0].replace('AM', ':00')
    #     return start_time + config.utc_offset
    #
    # def get_end_time(self, end_time):
    #     """#"""
    #     end_time = tuple(end_time.split('-'))[1].replace('PM', ':00')
    #     return end_time + config.utc_offset

    def is_only_by_appointment(self):
        return ''

    def is_or_by_appointment(self):
        return ''

    def is_subject_to_change(self):
        # create conditional when/if column is present
        return ''

    def get_start_date(self, start_date, county):
        string = str(start_date)
        date = datetime.datetime.strptime(string, '%m/%d/%Y').strftime('%Y-%m-%d')
        offset = self.utc_offset(county)
        return date + offset
        # return start_date + config.utc_offset

    def get_end_date(self, end_date, county):
        # create conditional when/if column is present
        string = str(end_date)
        date = datetime.datetime.strptime(string, '%m/%d/%Y').strftime('%Y-%m-%d')
        offset = self.utc_offset(county)
        return date + offset

    def get_hours_open_id(self, hours_open_id):
        """#"""
        return hours_open_id

    def create_schedule_id(self, index):
        """Create id"""
        # concatenate county name, or part of it (first 3/4 letters) with index
        # add leading zeros to maintain consistent id length
        if index <= 9:
            index_str = '000' + str(index)

        elif index in range(10, 100):
            index_str = '00' + str(index)

        elif index in range(100, 1000):
            index_str = '0' + str(index)
        else:
            index_str = str(index)

        return 'sch' + str(index_str)

    def build_schedule_txt(self):
        """
        New columns that match the 'schedule.txt' template are inserted into the DataFrame, apply() is
        used to run methods that generate the values for each row of the new columns.
        """

        self.base_df['start_time2'] = self.base_df.apply(
            lambda row: self.get_sch_start_time(row["times"], row['county']), axis=1)

        self.base_df['end_time2'] = self.base_df.apply(
            lambda row: self.get_sch_end_time(row['times'], row['county']), axis=1)
        #
        self.base_df['is_only_by_appointment2'] = self.base_df.apply(
            lambda row: self.is_only_by_appointment(), axis=1)

        self.base_df['is_or_by_appointment2'] = self.base_df.apply(
            lambda row: self.is_or_by_appointment(), axis=1)

        self.base_df['is_subject_to_change2'] = self.base_df.apply(
            lambda row: self.is_subject_to_change(), axis=1)
        #
        self.base_df['start_date2'] = self.base_df.apply(
            lambda row: self.get_start_date(row['start_date'], row['county']), axis=1)
        #
        self.base_df['end_date2'] = self.base_df.apply(
            lambda row: self.get_end_date(row['end_date'], row['county']), axis=1)
        #
        self.base_df['hours_open_id2'] = self.base_df.apply(
            lambda row: self.get_hours_open_id(row['hours_open']), axis=1)
        #
        self.base_df['id2'] = self.base_df.apply(
            lambda row: self.create_schedule_id(row['index']), axis=1)

        return self.base_df

    #    def dedupe(self, dupe):
    #        """#"""
    #        return dupe.drop_duplicates(subset=['address_line', 'hours'])

    def write_schedule_txt(self):
        """Drops base DataFrame columns then writes final dataframe to text or csv file"""

        sch = self.build_schedule_txt()

        # start_time2, end_time2, is_only_by_appointment2, is_or_by_appointment2, is_subject_to_change2, start_date2, end_date2, hours_open_id2, id2

        # Drop base_df columns.
        sch.drop(['county', 'officer', 'email', 'blank', 'phone', 'fax', 'address_one',
                  'address_two', 'city', 'state', 'zip', 'times', 'start_date', 'end_date', 'index', 'time_zone',
                  'address_line', 'directions', 'hours', 'photo_uri', 'hours_open', 'is_drop_box', 'is_early_voting',
                  'latitude', 'longitude', 'latlng_source', 'id'], inplace=True,
                 axis=1)

        # hours,photo_uri,hours_open_id,is_drop_box,is_early_voting,latitude,longitude,latlng_source,id,

        # Drop base_df columns.
        # sch.drop(['address_line', 'directions', 'hours', 'photo_uri', 'is_drop_box', 'is_early_voting',
        #          'latitude', 'longitude', 'latlng_source', 'id'], inplace=True, axis=1)

        # sch = self.dedupe(sch)  # 'address_line' and 'hours are used to identfy/remove duplicates
        # print sch

        # sch.drop(['address_line', 'hours'], inplace=True, axis=1)
        # print sch

        sch.rename(columns={'start_time2': 'start_time', 'end_time2': 'end_time',
                            'is_only_by_appointment2': 'is_only_by_appointment',
                            'is_or_by_appointment2': 'is_or_by_appointment',
                            'is_subject_to_change2': 'is_subject_to_change',
                            'start_date2': 'start_date', 'end_date2': 'end_date',
                            'hours_open_id2': 'hours_open_id', 'id2': 'id'}, inplace=True)

        print sch

        sch.to_csv(config.polling_location_output + 'schedule.txt', index=False, encoding='utf-8')  # send to txt file
        sch.to_csv(config.polling_location_output + 'schedule.csv', index=False, encoding='utf-8')  # send to csv file


if __name__ == '__main__':
    early_voting_true = 'true'  # true or false
    # drop_box_true =
    # state_file = 'kansas_early_voting_info.csv'
    #
    # early_voting_file = "/Users/danielgilberg/Development/hand-collection-to-vip/polling_location/polling_location_input/" + state_file
    #
    # early_voting_file = config.schedule_data

    file = "intermediate_pl_for_sch.csv"
    early_voting_file = config.polling_location_output + file


    colnames = ['county', 'officer', 'email', 'blank', 'phone', 'fax', 'address_one',
                'address_two', 'city', 'state', 'zip', 'times','start_date', 'end_date', 'time_zone', 'index',
                'address_line', 'directions', 'hours', 'photo_uri', 'hours_open', 'is_drop_box',
                'is_early_voting', 'latitude', 'longitude', 'latlng_source', 'id']

    early_voting_df = pd.read_csv(early_voting_file, names=colnames, encoding='utf-8', skiprows=1)

    # early_voting_df['index'] = early_voting_df.index + 1

    ScheduleTxt(early_voting_df).write_schedule_txt()
    # ScheduleTxt(early_voting_df).format_for_schedule()
