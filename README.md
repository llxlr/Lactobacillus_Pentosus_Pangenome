# Lactobacillus Pentosus Pangenome

> 戊糖乳杆菌泛基因组分析

## 工作流程

### 1. 下载、解压序列文件：

```bash
$ cd ./sequence/origin/
$ wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/641/185/GCA_003641185.1_ASM364118v1/GCA_003641185.1_ASM364118v1_genomic.fna.gz -O DSM20314.fna.gz
$ wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/850/015/GCA_002850015.1_ASM285001v1/GCA_002850015.1_ASM285001v1_genomic.fna.gz -O BGM48.fna.gz
$ wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/627/295/GCA_003627295.1_ASM362729v1/GCA_003627295.1_ASM362729v1_genomic.fna.gz -O ZFM222.fna.gz
$ wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/627/375/GCA_003627375.1_ASM362737v1/GCA_003627375.1_ASM362737v1_genomic.fna.gz -O ZFM94.fna.gz
$ wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/211/885/GCA_002211885.1_ASM221188v1/GCA_002211885.1_ASM221188v1_genomic.fna.gz -O SLC13.fna.gz
$ for file in *.fna.gz;do gzip -d $file;done # 解压
$ cd -
```

### 2. 格式化`FASTA`序列文件为`Contig`叠连群序列文件

根据长度或给定的定义列表删除叠连群，以更简单的名称生成输出

```bash
$ for file in ./sequence/origin/*.fna;do
> anvi-script-reformat-fasta ${file} -o \
> $(echo ${file} | sed 's/origin/contigs/g' | sed 's/\.fna/\.contig\.fna/g') \
> --simplify-name
> done
```

- `-o`：指定输出文件名称
- `--simplify-name`：顾名思义就是以更简单的名称输出

### 3. 生成`Contig`叠连群数据库

叠连群数据库将保留与叠连群相关的所有信息：开放阅读框的位置，每个叠连群的`K-MER`频率，其中拆分开始和结束，功能和基因的分类注释等。

```bash
$ for file in ./sequence/contig/*.contig.fna;do
> anvi-gen-contigs-database -f ${file} -o \
> $(echo ${file}|sed 's/sequence\/contig/databases/g'|sed 's/\.contig\.fna/.db/g'|sed 's/ //g')
> -n "Lactobacillus Pentosus Pangenome"
> done
```

- `-o`：指定输出文件名称
- `-n`：指定项目名称

### 4. `hmms`搜索和鉴定单拷贝基因

`HMM`：隐马尔科夫模型。它使用`HMMER`识别用户基因中与多个默认的细菌单拷贝核心基因集合的命中率。

```bash
$ for file in ./databases/*.db;do
> anvi-run-hmms -c ${file} \
>               -T 10 \
>               --just-do-it \
>               --queit
> done
```

- `-T`：指定线程数
- `--just-do-it`：如果存在运行过hmms的数据库，会强制再次重新执行
- `--queit`：静默运行命令

### 5.数据库迁移

```shell
$ anvi-migrate --migrate-dbs-safely ./databases/*.db
```

### 6. 生成基因组存储

```shell
$ anvi-gen-genomes-storage -e ./databases/external-genomes.csv -o ./databases/LP-GENOMES.db
```

- `-e`：指定外部基因组文件
- `-o`：指定输出基因组存储文件

### 7. 运行泛基因组分析

```shell
$ anvi-pan-genome -g .databases/LP-GENOMES.db \
                  -n "Lactobacillus_Pentosus_Pangenome" \
                  -o LP \
                  -T 10 \
                  --minbit 0.5 \
                  --mcl-inflation 10 \
                  --use-ncbi-blast
```

- `-n`：指定项目名称
- `-o`：指定输出目录名称
- `-T`：指定线程数
- `--minbit`：使用最初在[ITEP](http://bmcgenomics.biomedcentral.com/articles/10.1186/1471-2164-15-8)中实现的最小位启发式算法来消除两个氨基酸序列之间的弱匹配，默认最小位为0.5。
- `--mcl-inflation`：使用[MCL](http://www.ncbi.nlm.nih.gov/pubmed/22144159)算法在氨基酸序列相似性搜索结果中识别簇。若比较许多远缘基因组（即基因组分为不同家族或更远的基因组），使用`2`，若比较非常密切相关的基因组（相同物种的菌株），则使用`10`。
- `--use-ncbi-blast`：使用NCBI的`blastp`进行氨基酸序列相似性搜索。

### 8. 数据可视化

如果运行过泛基因组分析，可以直接运行可视化。

```shell
$ anvi-display-pan -g ./databases/LP-GENOMES.db \
                   -p LP/Lactobacillus_Pentosus_Pangenome-PAN.db \
                   -I localhost \
                   --title "Lactobacillus Pentosus Pangenome"
```

- `-g`：指定基因组存储文件
- `-p`：指定运行泛基因组分析后的数据库文件
- `-I`：指定访问地址。`localhost`或`127.0.0.1`都能本地访问
- `--title`：项目名称

## 更多

- [Anvi’o折腾记录和学习](anvio.md)

