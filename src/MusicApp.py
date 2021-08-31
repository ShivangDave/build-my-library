from ytmusicapi import YTMusic
import csv
import time

class MusicApp:

    def __init__(self):
        self.context = YTMusic('./src/headers_auth.json')

    def seed_data(self):
        file_name = "songs.csv"
        rows = []

        with open(file_name,'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                rows.append(row[0])

        failed = []
        new_playlist = self.context.create_playlist('Imported Songs','Youtube API Test!!')
        file = open("failed_songs.txt","w")
        count = 0

        for i in rows:
            count += 1
            song_results = self.context.search(i,'songs')

            if len(song_results) > 0:
                if i != song_results[0]['title']:
                    video_result = self.context.search(i,'videos')
                    if len(video_result) > 0:
                        # print(video_result[0]['videoId'])
                        print(str(count) + "/" + str(len(rows)))
                        self.context.add_playlist_items(new_playlist,[video_result[0]['videoId']])
                    else:
                        print("Failed: " + str(len(failed) + 1) + "/" + str(len(rows)))
                        failed.append(i)
                        file.write(i + ' \n')
                else:
                    # print(song_result[0]['videoId'])
                    print(str(count) + "/" + str(len(rows)))
                    self.context.add_playlist_items(new_playlist,[song_result[0]['videoId']])
            else:
                print("Failed: " + str(len(failed) + 1) + "/" + str(len(rows)))
                failed.append(i)
                file.write(i + ' \n')

        file.close()
