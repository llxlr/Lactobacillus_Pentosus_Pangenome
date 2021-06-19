#!/usr/bin/env bash
set -eu

genomes='./sequence/origin/'
contigs='./sequence/contigs/'
databases='./databases/'

for genome in $(ls ${genomes});
do
    contigs_genome=${contigs}$(echo ${genome}|sed 's/\.fna/\.contigs\.fna/g');
    # fasta file => contigs-fasta file
    if [ ! -f ${contigs_genome} ];
    then
        anvi-script-reformat-fasta ${genomes}${genome} -o ${contigs_genome} --simplify-name;
        echo ${contigs_genome}'已创建！'
    else
        echo 'contigs-fasta文件已存在！';
    fi
    # contigs-fasta file => sqlite database file
    db_file=${databases}$(echo ${genome}|sed 's/\.fna/\.db/g');
    if [ ! -f ${db_file} ];
    then
        anvi-gen-contigs-database -f ${contigs_genome} -o ${db_file};
        echo ${db_file}'已创建！';
    else
        echo '数据库文件已存在！';
    fi
done

cd ${databases}
pwd
anvi-migrate --migrate-dbs-safely *.db;
anvi-gen-genomes-storage -e external-genomes.csv -o PROCHLORO-GENOMES.db;
cd -

