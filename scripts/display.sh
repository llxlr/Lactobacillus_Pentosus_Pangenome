#!/usr/bin/env bash
# 参考脚本：https://github.com/merenlab/anvio/blob/master/anvio/tests/run_pangenome_tests.sh
set -eu

genomes='./sequence/origin/'
contigs="./sequence/contig/"
databases="./databases/"
threads=$1

INFO() {
    echo -e "\033[1;30m\033[47m:: $1 ...\033[0m";
}

# 下载、解压序列
if (($(find ${genomes} -name "*.fna"|wc -l) != 5))
then
    INFO "下载原始序列文件"
    
    wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/641/185/GCA_003641185.1_ASM364118v1/GCA_003641185.1_ASM364118v1_genomic.fna.gz -O ${genomes}DSM20314.fna.gz
    wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/850/015/GCA_002850015.1_ASM285001v1/GCA_002850015.1_ASM285001v1_genomic.fna.gz -O ${genomes}BGM48.fna.gz
    wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/627/295/GCA_003627295.1_ASM362729v1/GCA_003627295.1_ASM362729v1_genomic.fna.gz -O ${genomes}ZFM222.fna.gz
    wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/627/375/GCA_003627375.1_ASM362737v1/GCA_003627375.1_ASM362737v1_genomic.fna.gz -O ${genomes}ZFM94.fna.gz
    wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/211/885/GCA_002211885.1_ASM221188v1/GCA_002211885.1_ASM221188v1_genomic.fna.gz -O ${genomes}SLC13.fna.gz

    for file in ${genomes}*.fna.gz
    do
	INFO "解压${file}"
	gzip -d ${file}
    done

else
    INFO "存在原始序列文件"
fi

# 格式化序列
for genome in $(ls ${genomes});
do
    contigs_genome=${contigs}$(echo ${genome}|sed "s/\.fna/\.contigs\.fna/g")
    
    INFO "原始序列文件 => 重叠群序列文件"
    if [ ! -f ${contigs_genome} ]
    then
        anvi-script-reformat-fasta ${genomes}${genome} -o ${contigs_genome} --simplify-name
        echo ${contigs_genome}"已创建！"
    else
	echo ${contigs_genome}"文件已存在！"
    fi
    echo

    INFO "重叠群序列文件 => 重叠群数据库"
    db_file=${databases}$(echo ${genome}|sed "s/\.fna/\.db/g")
    if [ ! -f ${db_file} ]
    then
        anvi-gen-contigs-database -f ${contigs_genome} -o ${db_file}
        echo ${db_file}"已创建！"
    else
        echo ${db_file}"文件已存在！"
    fi
    echo

    INFO "静默运行HMMS"
    anvi-run-hmms -c ${db_file} \
	    -T ${threads} \
	    --just-do-it \
	    --quiet
    echo
done

INFO "数据库迁移"
anvi-migrate --migrate-dbs-safely ${databases}*.db;
echo

INFO "生成基因组存储"
anvi-gen-genomes-storage -e ${databases}external-genomes.csv -o ${databases}LP-GENOMES.db;
echo

INFO "运行泛基因组分析"
anvi-pan-genome -g ${databases}LP-GENOMES.db \
		-n "Lactobacillus_Pentosus_Pangenome" \
		-o LP \
		-T ${threads} \
		--minbit 0.5 \
		--mcl-inflation 10 \
		--use-ncbi-blast
echo

# INFO "添加额外层数据"
# anvi-import-misc-data ${databases}layer-additional-data.txt \
# 			-p LP/Lactobacillus_Pentosus_Pangenome-PAN.db \
# 			--target-data-table layers
# echo

INFO "可视化数据"
anvi-display-pan -g ${databases}LP-GENOMES.db \
		 -p LP/Lactobacillus_Pentosus_Pangenome-PAN.db \
		 -I localhost \
		 --title "Lactobacillus Pentosus Pangenome"

