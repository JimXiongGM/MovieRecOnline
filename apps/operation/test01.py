from pyspark import SQLContext, SparkContext, SparkConf
from pyspark.sql import SparkSession
import pyspark
sc = SparkContext(appName="pyspark mysql demo")
sqlContext = SQLContext(sc)

# 创建连接获取数据
df_movie=sqlContext.read.format("jdbc").option("url", "jdbc:mysql://localhost:3308/meich_db")\
.option("dbtable", "tq2").option("user", "root").option("password", "Mysql_08").load()
 
def onehotencode(df, s1, s2, temp):
    from pyspark.ml.feature import OneHotEncoder, StringIndexer
    stringIndexer = StringIndexer(inputCol=s1, outputCol=temp)
    model = stringIndexer.fit(df)
    indexed = model.transform(df)

    encoder = OneHotEncoder(inputCol=temp, outputCol=s2)
    encoded = encoder.transform(indexed)
    encoded.select(s2).show()
    return encoded
    
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import ArrayType, StringType

def tolistbycom(s):
    result = s.split(',')
    return result

def tolistbyslash(s):
    result = s.split('\\')
    return result


tolistbycomUDF=UserDefinedFunction(tolistbycom, ArrayType(StringType())) 
tolistbyslashUDF=UserDefinedFunction(tolistbyslash, ArrayType(StringType())) 


df_tags = df_wri.withColumn('tags',tolistbycomUDF('mv_type'))
df_stars = df_tags.withColumn('stars', tolistbyslashUDF('mv_star'))

from pyspark.ml.feature import CountVectorizer

# Add binary=True if needed
df_l1 = (CountVectorizer(inputCol="stars", outputCol="star_vector")
    .fit(df_stars)
    .transform(df_stars))
df_l2 = (CountVectorizer(inputCol="tags", outputCol="tag_vector")
    .fit(df_l1)
    .transform(df_l1))

import jieba
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import StringType

def seg(s):
    fenci_text = jieba.cut(s)
    result = " ".join(fenci_text)
    return result

# 根据python的返回值类型定义好spark对应的数据类型
# python函数中返回的是string，对应的pyspark是StringType
segUDF=UserDefinedFunction(seg, StringType()) 
# 使用自定义函数
# df_seg = df_movie.withColumn('introduction',segUDF('mv_introduction'))


def word2vec(df, inputcol, outputcol, vecsize):
    from pyspark.mllib.feature import Word2Vec
    from pyspark.ml.feature import Word2Vec
    from pyspark.ml.feature import CountVectorizer, CountVectorizerModel, Tokenizer, RegexTokenizer, StopWordsRemover
    # 使用自定义函数
    df.drop('seg')
    df_seg = df.withColumn("seg",segUDF(inputcol))
    df_w = df_seg.drop('words')
    tokenizer = Tokenizer(inputCol=inputcol, outputCol='words')
    t_words = tokenizer.transform(df_w)
    t_words.select('words').head()
    #4.将文本向量转换成稀疏表示的数值向量（字符频率向量）
    cv = CountVectorizer(inputCol="words", outputCol="features", vocabSize=5, minDF=2.0)
    df_f = t_words.drop("features")
    cv_model = cv.fit(df_f)
    cv_result = cv_model.transform(df_f)
    #5.将tokenizer得到的分词结果转换数字向量
    word2Vec = Word2Vec(vectorSize=vecsize, minCount=0, inputCol="words", outputCol=outputcol)
    w2v_model = word2Vec.fit(cv_result)
    result = w2v_model.transform(cv_result)
    for feature in result.select(outputcol).take(3):
        print(feature)
        return t_words
        
df_title = word2vec(df_l2, "ztitle", "title_vec", 100)

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler

assembler = VectorAssembler(
    inputCols=["direcVec","counVec","wriVec","star_vector","tag_vector"],
    outputCol="features")

output = assembler.transform(df_title)
output.select("features").show(truncate=False)

from pyspark.ml.feature import Normalizer
normalizer = Normalizer(inputCol="features", outputCol="norm", p=2.0)
data = normalizer.transform(output)

import pyspark.sql.functions as psf
from pyspark.sql.types import DoubleType
dot_udf = psf.udf(lambda x,y: float(x.dot(y)), DoubleType())
similarity = data.alias("i").join(data.alias("j"), psf.col("i.ID") < psf.col("j.ID"))\
    .select(
        psf.col("i.ID").alias("i"), 
        psf.col("j.ID").alias("j"), 
        dot_udf("i.norm", "j.norm").alias("dot"))\
    .sort("i", "j")


# 创建连接写入数据
similarity.write.format("jdbc").option("url", "jdbc:mysql://localhost:3308/meich_db")\
.option("dbtable", "similarity02").option("user", "root").option("password", "Mysql_08").mode('append').save()

def main():
    pass









