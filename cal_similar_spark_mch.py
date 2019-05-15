""" 
@author: Mei CH
@contact: 1532744860@qq.com
@software: jupyter
@time: 19-5-10 9:00am
"""

import pyspark
from pyspark import HiveContext, SQLContext, SparkContext, SparkConf
from pyspark.sql.types import StringType,DoubleType
import pyspark.sql.functions as psf
# from pyspark.mllib.feature import Word2Vec
from pyspark.ml.feature import *
import jieba

def onehotencode(df, s1, s2, temp):
    from pyspark.ml.feature import OneHotEncoder, StringIndexer
    stringIndexer = StringIndexer(inputCol=s1, outputCol=temp)
    model = stringIndexer.fit(df)
    indexed = model.transform(df)
    encoder = OneHotEncoder(inputCol=temp, outputCol=s2)
    encoded = encoder.transform(indexed)
    encoded.select(s2).show()
    return encoded
    

def seg(s):
    fenci_text = jieba.cut(s)
    result = " ".join(fenci_text)
    return result


def word2vec(df, inputcol, outputcol):
    # 使用自定义函数
    df_seg = df.withColumn(inputcol,segUDF(inputcol))
    df_seg.drop('words')
    tokenizer = Tokenizer(inputCol=inputcol, outputCol='words')
    t_words = tokenizer.transform(df_seg)
    t_words.select('words').head()
    #4.将文本向量转换成稀疏表示的数值向量（字符频率向量）
    cv = CountVectorizer(inputCol="words", outputCol="features", vocabSize=5, minDF=2.0)
    t_words.drop("features")
    cv_model = cv.fit(t_words)
    cv_result = cv_model.transform(t_words)
    #5.将tokenizer得到的分词结果转换数字向量
    word2Vec = Word2Vec(vectorSize=100, minCount=0, inputCol="words", outputCol=outputcol)
    w2v_model = word2Vec.fit(cv_result)
    result = w2v_model.transform(cv_result)

def run_similar(mysql_user,mysql_pwd,mysql_host,mysql_db,kaiguan=1):

    sc = SparkContext(appName="calculate similar matrix" , master="spark://master:7077")
    sqlContext = SQLContext(sc)

    # 创建连接获取数据
    # DataFrame 

    df_movieinfo = sqlContext.read.format("jdbc")\
            .option("url", "jdbc:mysql://"+mysql_host+":3306/"+mysql_db)\
            .option("dbtable", "movies_movieinfo")\
            .option("user", mysql_user)\
            .option("password",mysql_pwd)\
            .load()
    stringIndexer = StringIndexer(inputCol="directors", outputCol="director_Index")
    model = stringIndexer.fit(df_movieinfo)
    indexed = model.transform(df_movieinfo)

    encoder = OneHotEncoder(inputCol="director_Index", outputCol="direcVec")
    encoded = encoder.transform(indexed)
    encoded.select('direcVec').show()


    # 根据python的返回值类型定义好spark对应的数据类型
    # python函数中返回的是string，对应的pyspark是StringType
    segUDF = psf.UserDefinedFunction(seg, StringType()) 
    
    # 使用withColumn函数增加列
    df_seg = df_movieinfo.withColumn('description_2',segUDF('description'))

    # word2vec(df_movieinfo, "description", "result")
    #3.使用tokenizer分词
    tokenizer = Tokenizer(inputCol="description_2", outputCol="words")
    t_words = tokenizer.transform(df_seg)



    if kaiguan == 0 :
        hashingTF = HashingTF(inputCol="words", outputCol="rawFeatures", numFeatures=100)
        featurizedData = hashingTF.transform(t_words)
        idf = IDF(inputCol="rawFeatures", outputCol="features")
        idfModel = idf.fit(featurizedData)
        normalizer = Normalizer(inputCol="features", outputCol="norm", p=2.0)
        dot_udf = psf.udf(lambda x,y: float(x.dot(y)), DoubleType())
        rescaledData = idfModel.transform(featurizedData)
        df_norm = normalizer.transform(rescaledData)
        # ??
        similarity_idf = df_norm.alias("item1").join(df_norm.alias("item2"), psf.col("item1.ID") < psf.col("item2.ID"))\
            .select(
                psf.col("item1.ID").alias("item1"), 
                psf.col("item2.ID").alias("item2"), 
                dot_udf("item1.norm", "item2.norm").alias("similar"))\
            .sort("item1", "item2")
       # 创建连接写入数据
        similarity_idf.write.format("jdbc").option("url", "jdbc:mysql://"+mysql_host+":3306/"+mysql_db)\
        .option("dbtable", "xxxxxxxxx").option("user", mysql_user).option("password",mysql_pwd).mode('append').save()
        
    elif kaiguan == 1 :
    
        #4.将文本向量转换成稀疏表示的数值向量（字符频率向量）
        cv = CountVectorizer(inputCol="words", outputCol="features", vocabSize=5, minDF=2.0)
        cv_model = cv.fit(t_words)
        cv_result = cv_model.transform(t_words)
        #5.将tokenizer得到的分词结果转换数字向量
        word2Vec = Word2Vec(vectorSize=100, minCount=0, inputCol="words", outputCol="result")
        w2v_model = word2Vec.fit(cv_result)
        result = w2v_model.transform(cv_result)
        normalizer = Normalizer(inputCol="result", outputCol="norm", p=2.0)
        data = normalizer.transform(result)
        dot_udf = psf.udf(lambda x,y: float(x.dot(y)), DoubleType())
        similarity_w2v = data.alias("item1").join(data.alias("item2"), psf.col("item1.ID") < psf.col("item2.ID"))\
            .select(
                psf.col("item1.ID").alias("item1"), 
                psf.col("item2.ID").alias("item2"), 
                dot_udf("item1.norm", "item2.norm").alias("dot"))\
            .sort("item1", "item2")

        # 创建连接写入数据
        similarity_w2v.write.format("jdbc")\
                .option("url", "jdbc:mysql://"+mysql_host+":3306/"+mysql_db)\
                .option("dbtable", "movies_moviesimilar_fromspark")\
                .option("user", mysql_user)\
                .option("password",mysql_pwd)\
                .mode('append').save()

if __name__ == '__main__':
    run_similar(mysql_user = "root",
                mysql_pwd = "candy5",
                mysql_host = "master",
                mysql_db = "MovieSizer")


