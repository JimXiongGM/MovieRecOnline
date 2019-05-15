'''
@author : Gong RY
'''
import MySQLdb
import distance


def run_cal():
    db = MySQLdb.connect(host="localhost", port=3308, user="root",
                         passwd="你的密码", db="MovieSizer", charset="utf8")
    cursor = db.cursor()
    sql = "select * from movies_movieinfo"
    cursor.execute(sql)
    res = cursor.fetchall()
    id = 1
    print('\n\n cal_similar_gry.py\n\n')
    # 控制矩阵规模
    for i in range(0, int(len(res)/100)):
        for j in range(i+1, len(res)):
            i_id = res[i][0]
            j_id = res[j][0]
            moviename_length = distance.levenshtein(res[i][1], res[j][1])
            nation_length = distance.levenshtein(res[i][3], res[j][3])
            directors_length = distance.levenshtein(res[i][4], res[j][4])
            leadactors_length = distance.levenshtein(res[i][5], res[j][5])
            editors_length = distance.levenshtein(res[i][6], res[j][6])
            length = moviename_length + nation_length + \
                directors_length + leadactors_length + editors_length
            similar = 1/length
            sql = "INSERT INTO movies_moviesimilar VALUES (%d, %d, %d, %f)" % (
                id, i_id, j_id, similar)
            cursor.execute(sql)
            db.commit()
            id = id + 1
        print('current : ', i)
    db.close()
    print('DONE !')


if __name__ == '__main__':
    run_cal()
