# Lactobacillus Pentosus Pangenome

> 戊糖乳杆菌泛基因组分析

1. 下载、解压序列文件：

```bash
$ cd ./sequence/origin/
$ wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/641/185/GCA_003641185.1_ASM364118v1/GCA_003641185.1_ASM364118v1_genomic.fna.gz -O "DSM 20314.fna.gz"
$ wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/850/015/GCA_002850015.1_ASM285001v1/GCA_002850015.1_ASM285001v1_genomic.fna.gz -O BGM48.fna.gz
$ wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/627/295/GCA_003627295.1_ASM362729v1/GCA_003627295.1_ASM362729v1_genomic.fna.gz -O ZFM222.fna.gz
$ wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/627/375/GCA_003627375.1_ASM362737v1/GCA_003627375.1_ASM362737v1_genomic.fna.gz -O ZFM94.fna.gz
$ wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/211/885/GCA_002211885.1_ASM221188v1/GCA_002211885.1_ASM221188v1_genomic.fna.gz -O SLC13.fna.gz
$ for file in *.fna.gz;do gzip -d $file;done
$ cd -
```

2. 格式化`FASTA`序列文件为`Contig`叠连群序列文件

```bash
$ for file in ./sequence/origin/*.fna;do
> anvi-script-reformat-fasta ${file} -o \
> $(echo ${file} | sed 's/origin/contigs/g' | sed 's/\.fna/\.contig\.fna/g') \
> --simplify-name
> done
```

3. 生成`Contig`叠连群数据库

```bash
$ for file in ./sequence/contig/*.contig.fna;do
> anvi-gen-contigs-database -f ${file} -o \
> $(echo ${file}|sed 's/sequence\/contig/database/g'|sed 's/\.contig\.fna/.db/g'|sed 's/ //g')
> done
```

`hmm`搜索和鉴定单拷贝基因

```bash
$ for file in ./database/*.db;do
> anvi-run-hmms -c ${file} --num-threads 10
> done
```

### 更多

- [Anvi’o折腾记录和学习](anvio.md)

