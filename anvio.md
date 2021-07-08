# Anvi’o折腾记录和学习

> [<img src="https://cdn.jsdelivr.net/gh/llxlr/cdn/img/2021/06/04/020611.jpeg" alt="星旅人" style="width: 30px;"/>](https://github.com/llxlr/Lactobacillus_Pentosus_Pangenome/)
>
> *2021.06.03~2021.06.08*
>
> *2021.06.19~2021.06.23*
>
> *2021.07.07~2021.07.08*

[toc]

## 安装

在`Ubuntu 20.04 LTS`里安装`anvi’o`，在`WSL2`中也适用。

### 使用`Docker`安装（最简单）

```bash
$ docker pull meren/anvio:7
$ docker run --rm -it -v 'pwd':'pwd' -w 'pwd' -p 8080:8080 meren/anvio:7
```

删除`anvi'o`：

```bash
$ docker system prune --force -a
```

如果还没有安装`Docker`，执行以下命令：

```bash
$ sudo apt-get update -y
$ sudo apt-get install apt-transport-https ca-certificates wget curl gnupg2 software-properties-common -y
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ echo "deb [arch=amd64] https://mirrors.bfsu.edu.cn/docker-ce/linux/ubuntu \
     $(lsb_release -cs) stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list
$ sudo apt-get update -y
$ sudo apt-get install docker-ce -y
```

使用`Docker`安装的最大缺陷是占用空间较大，`anvi'o`的`v7`版本镜像高达`14.4G`，就离谱。

### 使用`Conda`安装（最轻量）

（1）安装`Miniconda3`

```bash
$ sudo apt-get update -y
$ sudo apt-get install wget -y
$ wget https://mirrors.bfsu.edu.cn/anaconda/miniconda/Miniconda3-py38_4.9.2-Linux-x86_64.sh
$ sudo bash ./Miniconda3-py38_4.9.2-Linux-x86_64.sh
$ sudo chmod ugo+w -R /opt/minicnda3/  # 修改目录权限为所有用户都可写
```

（2）换源

这里抛弃经常使用的清华源，改用北外源。（北外源，永远滴神！）

```bash
$ conda config --set show_channel_urls yes
```

然后编辑用户目录生成的`.condarc`文件：

```bash
$ nano ~/.condarc
```

替换为以下内容：

```yaml
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/main
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/r
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.bfsu.edu.cn/anaconda/cloud
  msys2: https://mirrors.bfsu.edu.cn/anaconda/cloud
  bioconda: https://mirrors.bfsu.edu.cn/anaconda/cloud
  menpo: https://mirrors.bfsu.edu.cn/anaconda/cloud
  pytorch: https://mirrors.bfsu.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.bfsu.edu.cn/anaconda/cloud
```

修改后清除索引缓存：

```bash
$ conda clean -i
```

设置`pypi`源：

```bash
$ pip config set global.index-url https://mirrors.bfsu.edu.cn/pypi/web/simple
```

（3）安装依赖包及`anvi'o`

```bash
$ conda update conda -y  # 更新conda
$ conda update -n base -y --all  # 更新主环境所有包
```

使用`environment.yml`创建环境：

```bash
$ conda env create -f environment.yml
```

之后就不用下面的手动安装`conda`的包，继续编译安装其他包。

```bash
$ conda create -n anvio python=3.6 -y  # 创建python3.6的虚拟环境
$ conda activate anvio  # 激活虚拟环境
$ conda install -y -c bioconda \
  "sqlite >=3.31.1" \
  prodigal \
  mcl \
  muscle \
  hmmer=3.2.1 \
  diamond \
  blast \
  megahit \
  spades \
  #bowtie2 \  # 得手动安装
  bwa \
  #samtools \  # 得手动安装
  centrifuge \
  trimal \
  iqtree \
  trnascan-se \
  r-base \
  r-stringi \
  r-tidyverse \
  r-magrittr \
  r-optparse \
  r-gtools \
  bioconductor-qvalue \
  fasttree \
  fastani \
  pysam
$ conda install -y -c conda-forge h5py=2.8.0
$ conda install -y numpy scipy pandas matplotlib
```

安装`bowtie2`

```bash
$ wget https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.4/bowtie2-2.4.4-linux-x86_64.zip/download
$ unzip bowtie2-2.4.4-linux-x86_64.zip /opt/miniconda3/envs/anvio/bowtie2/

# export PATH="/opt/miniconda3/envs/anvio/bowtie2:$PATH"
$ source ~/.bashrc
$ bowtie2 -help
$ rm bowtie2-2.4.4-linux-x86_64.zip
```

安装`samtools`

```bash
$ wget https://github.com/samtools/samtools/releases/download/1.12/samtools-1.12.tar.bz2
$ tar jxvf samtools-1.12.tar.bz2
$ mkdir /opt/miniconda3/envs/anvio/samtools/
$ cd samtools-1.12/
$ sudo apt-get update
$ sudo apt-get install libbz2-dev liblzma-dev -y
$ ./configure --prefix=/opt/miniconda3/envs/anvio/samtools/
$ make && make install

# export PATH="/opt/miniconda3/envs/anvio/samtools/bin:$PATH"
$ source ~/.bashrc
$ samtools --help
$ cd .. && rm -rf samtools-1.12/ samtools-1.12.tar.bz2 
```

```bash
$ wget https://github.com/merenlab/anvio/releases/download/v7/anvio-7.tar.gz
$ pip install anvio-7.tar.gz
$ pip install mistune==0.8.4
$ rm anvio-7.tar.gz
```

安装自检：

```bash
$ anvi-self-test
```

conda装完只占用`3.2G`。

```bash
$ du -h -d 1 /opt/miniconda3/envs/
3.2G    /opt/miniconda3/envs/anvio
3.2G    /opt/miniconda3/envs
```

清理下载包

```bash
$ conda clean -y --all  # 清理所有下载包
$ cd /opt/miniconda3/pkgs/  # 进入下载目录
$ ls | xargs rm -rf  # 递归批量删除所有不包含空格的非隐藏文件及目录
```

## 使用

### [anvi-script-reformat-fasta](https://merenlab.org/software/anvio/help/7/programs/anvi-script-reformat-fasta/)

重新格式化 `FASTA` 文件（根据长度或给定的定义列表删除重叠群，以更简单的名称生成输出）。该程序将 `fasta` 文件转换为 `contigs-fasta`。 换句话说，它会重新格式化 `FASTA` 格式文件，以满足 `contigs-fasta` 所需的条件，其他 `anvi’o` 程序可以使用它。

```bash
$ anvi-script-reformat-fasta BGM48.fna -o BGM48.contigs.fna --simplify-name
```

> [`fasta`](https://merenlab.org/software/anvio/help/7/artifacts/fasta/): `FASTA` 格式的文件不一定符合 `contigs-fasta` 的标准。`anvi-script-reformat-fasta` 可以将常规 `fasta` 转换为 `contigs-fasta`，`anvi'o` 将能够更好地利用它。`fasta`可以是`.fna`、`.fasta`和`.fa`文件格式（甚至是`.txt`）。
>
> `contigs-fasta`是适合 `anvi-gen-contigs-database` 创建 `contigs-db` 的 `fasta` 文件。这个文件最关键的要求是它必须有简单的定义。 如果 `fasta` 文件没有简单的定义，则它不是一个合适的 `contigs-fasta`。 如果将此文件与 `anvi’o` 一起使用，则必须在映射之前修复原始 `FASTA` 文件。

> [重叠群（contig）](https://baike.baidu.com/item/%E9%87%8D%E5%8F%A0%E7%BE%A4)：彼此可以通过末端的重叠序列相互连接形成连续的DNA长片段的一组克隆。

### [anvi-gen-contigs-database](https://merenlab.org/software/anvio/help/7/programs/anvi-gen-contigs-database/)

 生成一个新的 `anvi'o` 重叠群数据库。

```bash
$ anvi-gen-contigs-database -f BGM48.contigs.fna -o BGM48.db
```

> `contigs-db`: 重叠群数据库是一个 anvi'o 数据库，其中包含与序列相关的关键信息。

### 其它

```bash
$ anvi-profile --version  # 查看当前anvi'o的版本
Anvi'o .......................................: hope (v7)

Profile database .............................: 35
Contigs database .............................: 20
Pan database .................................: 14
Genome data storage ..........................: 7
Auxiliary data storage .......................: 2
Structure database ...........................: 2
Metabolic modules database ...................: 2
tRNA-seq database ............................: 1
```

## 案例

### [宏基因组工作流程](https://merenlab.org/2016/06/22/anvio-tutorial-v2/)

所需文件：[`contigs.fa`](https://hub.fastgit.org/meren/anvio/raw/master/anvio/tests/sandbox/contigs.fa)、[`SAMPLE-01-RAW.bam`](https://hub.fastgit.org/meren/anvio/raw/master/anvio/tests/sandbox/SAMPLE-01-RAW.bam)、[`SAMPLE-02-RAW.bam`](https://hub.fastgit.org/meren/anvio/raw/master/anvio/tests/sandbox/SAMPLE-02-RAW.bam)和[`SAMPLE-03-RAW.bam`](https://hub.fastgit.org/meren/anvio/raw/master/anvio/tests/sandbox/SAMPLE-03-RAW.bam)

（1）重新格式化输入`FASTA`

```bash
$ anvi-script-reformat-fasta contigs.fa \
                             -o contigs-fixed.fa \
                             -l 0 \
                             --simplify-names
```

生成简化的`FASTA`序列。如果使用`--report-file`选项，还将创建一个制表符（TAB）分隔的文件，以便跟踪新文件中的哪条序列对应于原始文件中的偏转。

```bash
$ anvi-script-reformat-fasta contigs.fa \
                             -o contigs-fixed.fa \
                             -l 0 \
                             --report-file \
                             --simplify-names
```

此外还能从`contigs.fa`文件中删除一些非常短的重叠群，比如指定删除短于`1,000 nts`的序列：

```bash
$ anvi-script-reformat-fasta contigs.fa \
                             -o contigs-fixed.fa \
                             -l 1000 \
                             --simplify-names
```

（2）创建anvi’o重叠群数据库

`anvi'o`的重叠群数据库将保留与重叠群相关的所有信息：开放阅读框的位置，每个重叠群的K-MER频率，其中拆分开始和结束，功能和基因的分类注释等。重叠群数据库是与`anvi'o`宏基因组工作流程相关的、一切的基本组成部分。

创建重叠群数据库的最简单方法：

```bash
$ anvi-gen-contigs-database -f contigs.fa \
                            -o contigs.db \
                            -n 'An example contigs database'
```

（3）隐马尔科夫模型

虽然`anvi-run-hmms`绝对是可选项，但你不应该跳过这一步。Anvi'o可以用隐马尔科夫模型做很多事情（HMMs提供了统计手段，以概率术语对复杂数据进行建模，可用于搜索模式，这在生物信息学中效果很好，我们从已知序列中创建模型，然后在未知序列池中快速搜索这些模式以恢复命中率）。为了用平台上的HMM模型（在这一点上，它构成了多个已发表的细菌单拷贝基因集合）的命中率来装饰你的重叠群数据库，运行这个命令：

```bash
$ anvi-run-hmms -c contigs.db
```

- 它将利用多个默认的细菌单拷贝核心基因集合，并使用HMMER识别你的基因中与这些集合的命中率。如果你已经运行过一次，现在想添加一个你自己的HMM档案，这很容易。你可以使用`--hmm-profile-dir`参数来声明anvi'o应该在哪里寻找它。或者你可以使用`--installed-hmm-profile`参数，只在你的重叠群数据库上运行一个特定的默认HMM配置文件。
- 请注意，该程序默认只使用一个CPU，特别是如果你有多个CPU可用，你应该使用`--num-threads`参数。它大大改善了运行时间，因为HMMER确实是一个了不起的软件。

（4）可视化

```bash
$ anvi-display-contigs-stats contigs.db
```

（5）注释基因

另一个可选的步骤是运行`anvi-run-ncbi-cogs`程序，用NCBI的Clusters of Orthologus Groups的功能对contigs数据库中的基因进行注释。不要忘记使用`--num-threads`来指定你希望为此使用多少个核心。

> 如果第一次运行COGs，需要使用`anvi-setup-ncbi-cogs`在你的电脑上进行设置。只要在有互联网连接的机器上运行它。

（6）导入功能

Anvi'o还可以很好地利用你已经拥有的基因的功能注释。下面的文章介绍了将功能导入anvi'o的多种方法：[https://merenlab.org/2016/06/18/importing-functions/](https://merenlab.org/2016/06/18/importing-functions/)

（7）导入`taxonomy`

用分类法对基因进行注释可以使下游的事情更有意义，在某些情况下可能会改善人类引导的分选和细化步骤。请看这个帖子，了解实现这一目标的不同方法：[https://merenlab.org/2016/06/18/importing-taxonomy/](https://merenlab.org/2016/06/18/importing-taxonomy/)。然而，基因水平的分类法对于理解所产生的元基因组组装的基因组的分类法是不可靠的。

（8）配置BAM文件

未完待续……

### [无映射分箱](https://merenlab.org/2016/06/06/working-with-contigs-only/)

在[宏基因组工作流程](https://merenlab.org/2016/06/22/anvio-tutorial-v2/)中假设您有宏基因组短读。但如果拥有的只是一堆重叠群、基因组草图或MAG，而没有任何可映射的短读呢？关键是创建一个空白的Anvi’o配置文件数据库（profile database），与重叠群数据库（contigs database）一起使用。

#### 准备FASTA文件

此示例中，将下载[枯草芽孢杆菌](https://www.ncbi.nlm.nih.gov/bioproject/?term=ASM32874v1)（*Bacillus subtilis*）基因组，这是一种嵌合基因组（chimeric genome），从视觉上看会很有趣。

下载基因组：

```bash
$ wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/328/745/GCA_000328745.1_ASM32874v1/GCA_000328745.1_ASM32874v1_genomic.fna.gz -O Bacillus_subtilis.fna.gz
$ gzip -d Bacillus_subtilis.fna.gz
$ ls -lh Bacillus_subtilis.fna
-rwxrwxrwx 1 i i 7.4M May 13  2016 Bacillus_subtilis.fna
```

Anvi’o要求FASTA文件需要[简单的定义](https://merenlab.org/2016/06/22/anvio-tutorial-v2//#preparation)，而当前文件显然不符合该要求。

```bash
$ head -n 1 Bacillus_subtilis.fna
>AP012495.1 Bacillus subtilis BEST7613 DNA, complete genome
```

所以需要在生成重叠群数据库之前修复它。为此使用`anvi-script-reformat-fasta`程序，设置最小长度为`0`和`--simplify-names`选项。这样，脚本将不会删除FASTA文件中的任何内容，同时会转换成更简单的定义。

```bash
$ anvi-script-reformat-fasta Bacillus_subtilis.fna \
                             -o Bacillus_subtilis_fixed.fna \
                             -l 0 \
                             --simplify-names
Input ........................................: Bacillus_subtilis.fna
Output .......................................: fixed.fna
Minimum length ...............................: 0
Max % gaps allowed ...........................: 100.00%
Total num contigs ............................: 1
Total num nucleotides ........................: 7,585,470
Contigs removed ..............................: 0 (0.00% of all)
Nucleotides removed ..........................: 0 (0.00% of all)
Nucleotides modified .........................: 0 (0.00% of all)
Deflines simplified ..........................: True
```

这样看起来好极了：

```bash
$ head -n 1 Bacillus_subtilis_fixed.fna
>c_000000000001
```

接下来就是创建重叠群数据库。

#### 创建重叠群数据库

在此工作流程中创建重叠群数据库不同于其他工作流程：

（1）将设置一个比默认值更小的分割尺寸（因为我想看到一个更高度解决的基因组描述）

（2）将跳过细致的拆分，这样anvi’o不会在这种没有的东西上浪费时间

```bash
$ anvi-gen-contigs-database -f Bacillus_subtilis_fixed.fna \
                            -o Bacillus_subtilis.db \
                            -L 5000 \
                            --skip-mindful-splitting \
                            -n 'B. subtilis'
```

```text
CITATION
===============================================
Anvi'o will use 'prodigal' by Hyatt et al (doi:10.1186/1471-2105-11-119) to
identify open reading frames in your data. When you publish your findings,
please do not forget to properly credit their work.
```

然后在新生成的重叠群数据库中填充单拷贝的`gene hit tables`：

```bash
$ anvi-run-hmms -c Bacillus_subtilis.db
```

如果你正巧读了[这篇文章](https://merenlab.org/2015/12/07/predicting-number-of-genomes/)，你已经知道，在此时我们可以看一下该重叠群数据库中的细菌单拷贝基因的分布，并预测内部基因数量：

> 请使用`anvi-display-contigs-stats`程序了解在重叠群数据库中预测的细菌基因组、古基因组和真核基因组，以交互式显示这些数字。
>
> ```bash
> $ anvi-display-contigs-stats Bacillus_subtilis.db
> ```
>
> 还可以指定IP和端口：
>
> ```bash
> $ anvi-display-contigs-stats Bacillus_subtilis.db -I 127.0.0.1 -P 8000
> ```

```bash
$ anvi-script-gen_stats_for_single_copy_genes.py Bacillus_subtilis.db
$ anvi-script-gen_stats_for_single_copy_genes.R Bacillus_subtilis.db.hits Bacillus_subtilis.db.genes
```

#### 创建空白配置文件数据库

要可视化重叠群数据库，我们需要一个anvi’o配置文件数据库。但是如果没有映射数据来创建配置文件数据库，那该怎么办？使用`--blank-profile`参数运行`anvi-profile`：

```bash
$ anvi-profile -c Bacillus_subtilis.db \
               -o Bacillus_subtilis \
               -S Bacillus_subtilis \
               --blank-profile
```

生成的`Bacillus_subtilis/`文件夹里存放空白配置文件数据库、辅助的数据和运行日志：

```bash
$ ls Bacillus_subtilis/
AUXILIARY-DATA.db  PROFILE.db  RUNLOG.txt
```

生成了空白配置文件数据库后，便能够使用`anvi-interactive`可视化重叠群数据库中保存的内容。现在，可以使用实时完成/污染估计、存储和加载状态、创建集合并汇总它们进行分箱。

#### 可视化

一切都准备好开始以更好的方式启动Anvi'o交互式界面：

```bash
$ anvi-interactive -c Bacillus_subtilis.db \
                   -p Bacillus_subtilis/PROFILE.db
```

> 内树显示基于其四核苷酸频率剖面的该基因组中每种5kBP分裂的组织。 如您所见，树中有两个不同的分支。 其中一个分支可能代表综合症基因组，另一个代表枯草芽孢杆菌基因组Mitsuhiro Itaya等。 粗心地合并在一起。

为了清楚起见，这只是对数据最简单的样子，你还可以添加`--additional-view`或`--additional-layers`选项将更多数据信息添加到界面中，并对任何其他ANVI'O项目进行几乎做任何事情。作为示例，这里我将通过选择在这些不同分支中表示的分裂分离为不同的箱子，然后将我的选择存储到“集合”中来彼此分开，以便稍后总结。正如您所看到的，完成/冗余估计在单独选择时看起来要好得多。

#### 统计

现在可以统计一下存储在空白配置文件数据库中的集合：

```bash
$ anvi-summarize -c Bacillus_subtilis.db \
                 -p Bacillus_subtilis/PROFILE.db \
                 -C merens \
                 -o Bacillus_subtilis_summary
```

此总结的结果是静态HTML输出。

### [微生物泛基因组工作流程](https://merenlab.org/2016/11/08/pangenomics-v2/)

本节可获取的信息：

- 识别基因组之间的基因簇

- 将自己项目中宏基因组组装的基因组直接与其他来源的cultivar基因组结合

- 可视化基因组基因簇的分布

- 基于基因簇估算基因组间的关系

- 以交互方式（或编程方式）分箱基因簇到集合中和分箱总结

- 对给定的一组基因簇即时进行系统基因组分析

- 注释基因和检查基因簇中的氨基酸对齐

- 使用自己的基因组或基因簇的上下文信息扩展泛基因组

- 量化基因簇的几何和生化均匀性

- 对泛基因组中的基因组进行功能富集分析

- 计算和可视化基因组之间的平均核苷酸相似性分数

> Citation: If you use the anvi’o pangenomic workflow for your research, please consider citing [this work](https://peerj.com/articles/4320/) (which details the pangeomic workflows in anvi’o) in addition to [this one](https://peerj.com/articles/1319/) (which introduces the platform). Thank you for your consideration. 

Anvi’o泛基因组工作流由三个主要步骤组成：

1. 使用`anvi-gen-genomes-storage`程序生成Anvi’o基因组存储
2. 使用`anvi-pan-genome`程序生成Anvi’o泛数据库（需要上一步的基因组存储）
3. 使用`anvi-display-pan`程序展示结果（需要上两步的基因组存储和泛数据库）

然后，可以使用交互式界面分箱基因簇到集合中或者使用`anvi-import-collection`导入基因簇分箱，最后可以使用`anvi-summarize`程序创建结果的静态HTML摘要。

**依赖项**：

- DIAMOND和NCBI的blastp用于搜索

- MCL用于聚类

- muscle用于比对。是可选项。

> CITATION: Anvi'o will use 'muscle' by Edgar, doi:10.1093/nar/gkh340
(http://www.drive5.com/muscle) to align your sequences. If you publish your
findings, please do not forget to properly credit their work.

如果配置正确，运行以下命令将不会报错：

```bash
$ anvi-self-test --suite pangenomics
```

#### 生成anvi’o基因组存储

anvi’o基因组存储是一个专用数据库，用于存储有关基因组的信息。一个基因组存储可以仅由外部基因组、内部基因组或包含这两种类型的基因组生成。在进行下一步前，需要澄清这些定义：

- **外部基因组**是FASTA文件格式的任何内容（例如从NCBI下载或以任一种方式获得的基因组）。

- **内部基因组**是在宏基因组分析结束时储存在ANVI'O集合中的任何基因组分箱。

> **将Fasta文件转换为Anvi'o重叠群数据库**：当已经生成重叠群数据库和配置文件数据库时，操作内部基因组将非常简单。但是，如果仅拥有一堆Fasta文件，则必须将它们转换为重叠群数据库。有很多关于如何在[此处](https://merenlab.org/2016/06/22/anvio-tutorial-v2//#anvi-gen-contigs-database)创建一个重叠群数据库的信息，但如果觉得麻烦，也可以使用脚本`anvi-script-fasta-to-contigs-db`，这需要一个参数：Fasta 文件路径。高级用户可以查看源码，并根据需要编写批处理脚本（例如在运行HMMS时增加线程数）。还可以在重叠群数据库上运行`anvi-run-ncbi-cogs`以注释基因。

可以使用`anvi-gen-genomes-storage`程序创建基因组存储，这要求提供包含在此存储中的基因组的描述。外部基因组和内部基因组描述的文件格式略有不同。例如，这是一个`--external-genomes`文件：

| name    | contigs_db_path        |
| ------- | ---------------------- |
| Name_01 | /path/to/contigs-01.db |
| Name_02 | /path/to/contigs-02.db |
| Name_03 | /path/to/contigs-03.db |
| (…)     | (…)                    |

另一个是`--internal-genomes`文件：

| name    | bin_id    | collection_id | profile_db_path             | contigs_db_path             |
| ------- | --------- | ------------- | --------------------------- | --------------------------- |
| Name_01 | Bin_id_01 | Collection_A  | /path/to/profile.db         | /path/to/contigs.db         |
| Name_02 | Bin_id_02 | Collection_A  | /path/to/profile.db         | /path/to/contigs.db         |
| Name_03 | Bin_id_03 | Collection_B  | /path/to/another_profile.db | /path/to/another/contigs.db |
| (…)     | (…)       | (…)           | (…)                         | (…)                         |

> 对于第一列的`name`命名仅使用字母，数字和下划线。

这两个文件可以组合和分析`Anvi'o`集合和品种基因组中的基因组箱。对于基因组存储内一致性的最重要需求是确保每个内部和外部基因组在如何调用基因、如何分配功能等方面完全相同。`Anvi'o`会检查一些东西，但它不保证你不出错。例如，如果识别开放阅读框的基因调用者在所有重叠群中并不相同，则基因组存储中描述的基因不一定具有可比性。

一个硬核教程读者的实例：`原绿球藻泛基因组分析`

> 为了复现，接下来的教程将遵循一个实例。将简单创建31种原绿球藻分离体的泛基因组，基因组源于[本研究](https://peerj.com/articles/4320/)。打包数据：[doi:10.6084/m9.figshare.6318833](https://doi.org/10.6084/m9.figshare.6318833)。
>
> （1）数据预处理
>
> ```bash
> $ wget https://ndownloader.figshare.com/files/11857577 -O Prochlorococcus_31_genomes.tar.gz
> $ tar -zxvf Prochlorococcus_31_genomes.tar.gz
> $ mv ./Prochlorococcus_31_genomes ./genomes
> $ cd ./genomes
> $ anvi-migrate --migrate-dbs-safely *.db  # 数据库迁移
> Done! Your contigs db is now version 20...
> ...
> ```
>
> （2）泛基因组数据库的构建
>
> ```bash
> $ ls
> AS9601.db
> MIT9311.db
> ...
> ...
> SS51.db
> external-genomes.txt
> layer-additional-data.txt
> pan-state.json
> fix_functional_occurence_table.py
> ```
>
> 该目录包含重叠群数据库、外部基因组文件和包含每个基因组的其他信息、由制表符分隔的数据文件。生成基因组存储：
>
> ```bash
> $ anvi-gen-genomes-storage -e external-genomes.txt -o PROCHLORO-GENOMES.db
> ```
>
> 

#### 运行泛基因组分析

一旦准备好基因组存储，就可以使用`anvi-pan-genome`运行实际的泛基因组分析。这是此命令的最简单形式（伪命令，仅供展示）：

```bash
$ anvi-pan-genome -g MY-GENOMES.db -n PROJECT_NAME
```

> （3）泛基因组分析
>
> 接上一节，使用创建的31种原绿球藻分离体的基因组存储运行泛基因组：
>
> ```bash
> $ anvi-pan-genome -g PROCHLORO-GENOMES.db \
>                      --project-name "Prochlorococcus_Pan" \
>                      --output-dir PROCHLORO \
>                      --num-threads 12 \
>                      --minbit 0.5 \
>                      --mcl-inflation 10 \
>                      --use-ncbi-blast  # blastp
> ```
>
> `--projects-name`后面的选项都是可选的（包括对当前产物运行泛基因组的比对方式）。
>
> 解压目录还包含总结了每个基因组所属进化枝的`layer-additional-data.txt`文件（层额外数据），在计算泛基因组时将其添加到泛数据库中：
>
> ```bash
> $ anvi-import-misc-data layer-additional-data.txt \
>                            -p PROCHLORO/Prochlorococcus_Pan-PAN.db \
>                            --target-data-table layers  # 给基因组添加相关信息
> New layers additional data...
> ===============================================
> Data key "clade" .............................: Predicted type: str
> Data key "light" .............................: Predicted type: str
> 
> New data added to the db for your layers .....: clade, light.
> ```
>
> 我们都在寻找更丰富展示泛基因组的方法，`anvi'o`[额外数据表](http://merenlab.org/2017/12/11/additional-data-tables/)是很好的方法。

当运行`anvi-pan-genome`，程序将：

- 使用在基因组储存中的所有基因组。如果想专注于子集，可以使用`--genome-names`参数。

- 默认只使用单个核心。根据分析的基因组数量，此过程可能会非常耗时，可以考虑通过`--num-threads`参数增加使用线程数。

- 默认以“快”模式使用[DIAMOND](http://ab.inf.uni-tuebingen.de/software/diamond/)（或传递`--sensitive`参数使DIAMOND更敏捷）计算全部基因组中每种氨基酸序列的相似性，对比所有基因组中其他氨基酸序列（确保安装好DIAMOND）。或者，可以通过`--use-ncbi-blast`选项使用NCBI的`blastp`进行氨基酸序列相似性搜索。

> **注**：强烈建议使用`--use-ncbi-blast`选项进行分析。DIAMOND确实很快，使用`blastp`分析20\~30个基因组可能会花8\~9个小时（在标准笔记本电脑上使用单个核心），但速度的巨幅增加造成敏捷性和准确性降低。

- 使用每个基因调用，无论它们是否完整。尽管对于全基因组来说这不是一个大问题，但宏基因组组装的基因组 (MAG) 在重叠群的末尾和开头会有许多不完整的基因调用。到目前为止，实验表明它不会引起重大问题，但如果想排除它，可以使用`--exclude-partial-gene-calls`选项。
- 使用最初在[ITEP](http://bmcgenomics.biomedcentral.com/articles/10.1186/1471-2164-15-8)中实现的最小位启发式算法来消除两个氨基酸序列之间的弱匹配。泛基因组工作流首先通过进行相似性搜索来识别相似的氨基酸序列，然后根据这些相似性解析基因簇。在这种情况下，弱相似性可以连接不应该连接的基因簇。虽然网络分区算法可以从这些弱连接中恢复，但最好在每一步都尽可能多地消除噪声。因此，最小位启发式算法提供了一种方法来设置以消除两个氨基酸序列之间的弱匹配。我们从 ITEP 中学到了它，这是另一个针对泛基因组的综合分析工作流程，并决定使用它，因为它很有意义。简而言之，如果您有两个氨基酸序列 `A` 和 `B`，则最小位定义为`BITSCORE(A, B) / MIN(BITSCORE(A, A), BITSCORE(B, B))`。因此，如果两个序列之间的最小位得分在“较短”氨基酸序列的整个长度上非常相似，则为 1.0，如果与较短氨基酸序列的长度相比，它们在非常短的范围内匹配，则为 0.0 酸序列或序列同一性之间的匹配度低。默认最小位为 0.5，可以使用参数`--minbit`更改它。
- 使用[MCL](http://www.ncbi.nlm.nih.gov/pubmed/22144159)算法在氨基酸序列相似性搜索结果中识别簇。MCL膨胀参数默认使用`2` 。该参数定义了算法在基因簇识别过程中的敏感性。更高的敏感性意味着更多的簇，但当然更多的簇并不意味着更好地推断进化关系。有关此参数及其对簇粒度影响的更多信息，请访问[http://micans.org/mcl/man/mclfaq.html#faq7.2](http://micans.org/mcl/man/mclfaq.html#faq7.2)，但显然宏基因组学人员需要对此进行更多讨论。到目前为止，在Meren Lab中，如果我们比较许多远缘基因组（即基因组分为不同家族或更远的基因组），我们一直使用`2`，如果我们比较非常密切相关的基因组（即，相同物种的菌株），则使用`10`。也可以使用`--mcl-inflation`参数更改它。
- 利用每一个基因簇，即使它们在你的分析中只出现在一个基因组中。当然，单子singletons或双子doubletons的重要性将取决于你分析中的基因组数量，或你所考虑的问题。然而，如果你想定义一个截止点，你可以使用参数`--min-occurrence`，默认为`1`。增加这个分界线会提高聚类速度，使可视化更容易管理，但同样，这个参数应该根据每个研究的情况来考虑。
- 使用`欧氏距离`和`ward linkage`来组织基因簇和基因组。你可以用`--distance`和`--linkage`参数来改变这些。
- 如果已经有一个目录，尽量利用以前的搜索结果。这样你就可以使用`--minbit`、`--cl-inflation`或`--min-occurrence`参数，而不必重新进行氨基酸序列搜索。但如果你改变了一些东西，要么删除输出目录，要么使用`--overwrite-output-destinations`选项来重新搜索。

一旦做完这些，就会出现一个带有分析结果的新目录。可以使用[附加数据表子系统](https://merenlab.org/2017/12/11/additional-data-tables/)在泛基因组数据库中添加或删除附加数据项。

#### 展示泛基因组

一旦做完分析，便可以使用`anvi-display-pan`程序展示结果。

这是此命令的最简单形式（也是伪命令）：

```bash
$ anvi-display-pan -p PROJECT-PAN.db -g PROJECT-PAN-GENOMES.db
```

`anvi-display-pan`程序与`anvi-interactive`程序非常相似，欢迎界面无非是[标准的`anvi'o`交互式界面](https://merenlab.org/2016/02/27/the-anvio-interactive-interface//#using-the-anvio-interactive-interface)，为泛基因组分析略作调整。当然`anvi-display-pan`将允许你设置服务的IP地址和端口号，添加额外的视图数据、额外的图层和额外的树，等。运行`anvi-display-pan -h`查看帮助。

下面是在前几节中创建的31个原球菌分离体基因组的泛基因组：

```bash
$ anvi-display-pan -g PROCHLORO-GENOMES.db \
                   -p PROCHLORO/Prochlorococcus_Pan-PAN.db
```

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/prochlorococcus-pangenomics-raw.png)

看起来极丑但没关系。例如，为了改善一下情况，根据基因聚类的结果来组织基因组，从`Samples Tab > Sample Order`菜单中选择`gene_cluster frequencies`树。

<img src="https://merenlab.org/images/anvio/2016-11-08-pan-genomics/prochlorococcus-pangenomics-samples-tab.png" style="zoom:33%;" />

这是再次画它时发生的情况（注意右边出现的树）。

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/prochlorococcus-pangenomics-ordered.png)

看起来有点意思……但依然很丑。

这正是需要开始更有效地使用界面的地方。例如，这是使用交互式界面的设置面板中的额外设置项目进行一些改变后的同一个东西。

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/prochlorococcus-pangenomics-final.png)

如果你下载了原绿球藻数据包，显示`anvi'o状态文件`也在你的工作目录中，通过以下方式导入：

```bash
$ anvi-import-state -p PROCHLORO/Prochlorococcus_Pan-PAN.db \
                    --state pan-state.json \
                    --name default
```

#### 分割泛基因组

在某些情况下，人们可能想把一个给定的泛基因组分割成多个独立的泛基因组，比如一个只包含核心基因簇的泛基因组，或者一个只包含单子的泛基因组，等等。

Anvi'o用`anvi-split`程序来拆分东西，它也适用于泛数据库中的集合和分箱。它使你能够关注在一个给定的泛基因组中定义在一个分箱中的任何一组基因簇，并将它们分割成一个个独立的泛基因组。

如果你感到迷茫，你可能会发现这个功能的视觉描述要比技术描述更清晰。下面的步骤将用原绿球藻的泛基因组来演示。假定在原绿球藻的泛基因组中有三个分箱：Core、HL Core和Singletons，都存储在默认集合里：

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/splitting-pan-01.png)

这些分箱可以在此泛基因组中用`anvi-split`分割成它们自己的小型泛数据库。

```bash
$ anvi-split -p Prochlorococcus-PAN.db \
             -g Prochlorococcus-GENOMES.db \
             -C default \
             -o SPLIT_PANs
```

生成的目录将包含以下文件：

```bash
$ ls -lR SPLIT_PANs
total 0
drwxr-xr-x  3 meren  staff  96 Apr 26 16:37 Core
drwxr-xr-x  3 meren  staff  96 Apr 26 16:37 Hl_Core
drwxr-xr-x  3 meren  staff  96 Apr 26 16:37 Singletons

SPLIT_PANs/Core:
total 3240
-rw-r--r--  1 meren  staff  1658880 Apr 26 16:37 PAN.db

SPLIT_PANs/Hl_Core:
total 1560
-rw-r--r--  1 meren  staff  798720 Apr 26 16:37 PAN.db

SPLIT_PANs/Singletons:
total 4672
-rw-r--r--  1 meren  staff  1384448 Apr 26 16:37 PAN.db
```

这些是可以用`anvi-display-pan`可视化的独立泛基因组。例如运行以下命令：

```bash
$ anvi-display-pan -p SPLIT_PANs/Core/PAN.db \
                   -g Prochlorococcus-GENOMES.db
```

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/splitting-pan-02.png)

或者运行另一个：

```bash
$ anvi-display-pan -p SPLIT_PANs/Singletons/PAN.db \
                   -g Prochlorococcus-GENOMES.db
```

<img src="https://merenlab.org/images/anvio/2016-11-08-pan-genomics/splitting-pan-03.png"  />

#### 检查基因簇

在你的分析中，每一个基因簇都将包含一个或多个氨基酸序列，这些序列来源于一个或多个基因组。虽然可能会有一个“核心”部分，其中所有的基因簇都会出现在每个基因组中，但也经常会发现基因簇包含来自一个基因组的一个以上的基因调用（即一个特定基因组中的所有多拷贝基因最终都会出现在同一个基因簇中）。你迟早会开始对一些基因簇感到好奇，并想更多地了解它们。可以右键点击任何一个基因簇，会看到这个菜单（甚至可能更多）。

<img src="https://merenlab.org/images/anvio/2016-11-08-pan-genomics/pc-right-click.png" style="zoom:50%;" />

例如，如果你点击“Inspect gene cluster检查基因簇”，你会看到进入该基因簇的每个基因组的所有氨基酸序列（基因组的顺序和背景颜色与主显示中的排列相同）。

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/pc-inspect.png)

> 可以在[这里](http://merenlab.org/2018/02/13/color-coding-aa-alignments/)了解更多关于氨基酸颜色编码算法的信息

逐一浏览基因簇，有趣且很受教育。但是，如果想对大型选区进行理解，该怎么做？

正如你已经知道的，anvi'o的交互式界面允许你从树上进行选择。因此，你可以将基因簇的组别选择为分箱（不要介意左边面板上的数字，这显然是一个bug，在你的版本中会被修复）。

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/pc-selection.gif)

你可以创建多个有多种选择的分箱，如果你喜欢，甚至可以给它们起有意义的名字。

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/pc-collection.png)

虽然使用树枝图手动选择基因簇是一种选择，但也可以使用允许你定义且有非常具体搜索标准的搜索界面来识别它们。

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/search-gene-clusters.png)

你可以在界面中高亮显示这些选择，也可以将它们添加到一个集合中，以便日后进行总结。

此外，你还可以根据功能来搜索基因簇：

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/search-functions.png)



同样地，可以用你喜欢的任何名字将这些基因簇添加到集合中，并在以后对这些集合进行总结。

> 通过程序`anvi-get-sequences-for-gen-clusters`，也可以对基因簇进行高级访问。

#### 推断基因簇的同质性

基因簇很好，但不是所有的基因簇都是平等的。通过简单地检查几个基因簇中的排列组合，可以看到不同基因组中氨基酸序列之间不同程度的分歧。

> **同质性**（homogeneity）的概念：一个基因簇可能包含来自不同基因组的几乎相同的氨基酸序列，这将是一个高度同质的基因簇。另一个基因簇可能包含来自不同基因组的高度分歧的氨基酸序列，这将是一个高度非同质的基因簇，以此类推。人们可以通过关注序列排列的两个主要属性来推断基因簇内序列同质性的性质：功能同质性（即各基因间排列的氨基酸残基的保守程度）和几何同质性（即无论氨基酸的身份如何，基因簇内的间隙/残基分布是怎样的）。虽然通过手工检查基因簇内的对齐序列来了解基因簇的同质性是相当直接的，但还不可能自动量化这一信息。但是`anvi'o`现在提供了保障。事实上，了解基因簇内的同质性可以产生详细的生态或进化见解，了解在密切相关的类群中形成基因组背景的力量，或帮助进一步仔细检查基因簇，以进行人工或程序化的下游分析。本节目的是向你展示如何在`anvi'o`中解决这个问题，并证明其功效。

Anvi'o泛基因组包含两层总结每个基因簇的同质指数（功能和几何同质性估计）。

> 可以使用`anvi-compute-gen-cluster-homogeneity`程序将同质性估计添加到现有的`anvi'o`泛数据库中。

下面是原绿球藻泛基因组中的一个例子（见最外层的两个附加层）。

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/homogeneity-indices-main.png)

> **同质性指数**是根据排列组合来计算的。如果在一个基因簇中的某一组基因的排列由于某种原因而失败，那么它的同质性指数将显示为-1。

> `几何同质性指数`：表示一个基因簇的基因之间的几何配置程度。具体来说，我们要寻找基因簇的间隙/残基模式，这些模式是由排列组合确定的。根据定义，排列过程将基因的相似部分相互排列，并通过间隙字符表示缺失的残基（或基因上下文的不同结构配置）。如果缺口/残基分布模式在整个基因簇中大部分是均匀的，那么这个基因簇将具有较高的几何同质性，最大值为1.0，表明在排列中没有缺口。
>
> Anvi'o通过结合两个层面的基因簇内容的分析来计算几何同质性指数：站点层面的分析（即垂直排列的位置）和基因层面的分析（即水平排列的位置，因为它们是在同一个基因中）。我们将基因簇中的信息转换成二进制矩阵，其中间隙和残基简单地用1和0表示，我们利用异或逻辑运算符`xor`来识别和列举所有具有不同模式的比较。在位点水平的同质性检查中，该算法从左到右扫过，并识别出这些在对齐的列中的差异。在基因水平的同质性检查中，算法从一个基因扫到下一个基因，并识别一个基因中模式不一样的所有差异，有效地检查整个基因簇中的差距的扩散。可以用`--quick-homogeneity`参数跳过基因级的几何同质性计算。虽然这不会像默认方法那样准确或全面，但它可能会节省一些时间，这取决于你所处理的基因组的数量。

> `功能同质性指数`：相比之下，功能同质性指数考虑了对齐的残基（通过忽略间隙），并试图通过考虑不同残基的生化特性（这可能会影响基因在蛋白质水平上的功能保护）来量化一个站点中不同残基的差异。为了做到这一点，我们根据氨基酸的生化特性将其分为七个不同的 "保守组"。这些组是：非极性、芳香性、极性不带电、既有极性又有非极性特征（这些氨基酸也位于除此以外的组中）、酸性、碱性和大部分非极性（但包含一些极性特征）（更多信息请见[此文](https://merenlab.org/2018/02/13/color-coding-aa-alignments/)）。然后，该算法穿过整个基因群，根据氨基酸残基的生化特性的接近程度，给整个基因中同一位置的每一对氨基酸分配一个`0`到`3`的相似度分数。所有分配的相似性分数的总和表明了基因簇的功能同质性指数，如果所有的残基都是相同的，将达到其最大值1.0。
>
> 这两个指数都是在0到1的范围内，其中1是完全同质的，0是完全异质的。如果算法被运行时的错误打断（由于意外的问题，如由于某种原因不是所有的基因都是相同的长度，等等），它将默认指数的错误值为-1。因此，**如果你在摘要输出中看到-1**，这意味着我们由于某种原因未能对该基因簇中的排列组合进行理解
>
> > 在现实中，影响蛋白质折叠的复杂过程和氨基酸残基之间错综复杂的化学作用应该提醒我们，这些对相似性的评估只是单纯的数字建议，不一定能反映准确的生物化学见解，这不是这些同质性指数的目标。

在泛基因组中使用同质性指数：鉴于一切，让我们再看看自己的泛基因组。可以用这些同质性指数做很多事情。为快速了解一些同质性最低的基因簇，可以根据同质性的增加或减少来排列基因簇。比方说，我们想按照功能同质性的增加来排序（你可能已经知道，这可以通过主设置面板中的“项目顺序 Items order”组合框来完成）。

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/hi-order-01.png)

如果你打开显示屏右侧的“鼠标Mouse”面板，可以将鼠标悬停在该层上，看到所有基因簇的确切指数值。上图中光标下方显示的基因簇的功能同质性估计值相对较低，但几何同质性较高。我们可以检查一下这个基因簇，自己看一下：

<img src="https://merenlab.org/images/anvio/2016-11-08-pan-genomics/hi-inspect-01.png" style="zoom:33%;" />

你可以看到为什么相对较高的几何同质性分数是有意义的。这些基因中有三个具有相同的间隙/残基模式，而另一个基因末端的间隙使事情略有偏差，使几何得分接近0.75。另一方面，对齐的氨基酸的[颜色编码](https://merenlab.org/2018/02/13/color-coding-aa-alignments/)也给了我们一个关于它们之间缺乏功能同质性的提示。我们可以对几何同质性指数做同样的处理。自己尝试一下：根据几何同质性指数对泛基因组进行排序，并检查一个得分相对较低的基因簇。

那么，为了对我们的基因簇进行更深入的分析，我们可以做些什么？Anvi'o提供了相当强大的过滤基因簇的方法，既可以通过命令行程序`anvi-get-sequences-for-gen-clusters`，也可以通过界面对数据进行交互式探索：

<img src="https://merenlab.org/images/anvio/2016-11-08-pan-genomics/hi-search-pane-01.png" style="zoom: 25%;" />

`探索性分析`：假设你希望找到一个代表单拷贝核心基因的基因簇，其几何同质性与功能同质性之间的差异非常大。也就是说，你想要的东西在所有基因组中都是高度保守的，它在结构上受到限制，使它的排列保持同质性，但它有很大的空间以影响其功能异质性的方式进行多样化。你想要很多。但是anvi'o能做到吗？那么，对于这组非常特殊的约束条件，你可以先根据递减的几何同质性指数对所有的基因簇进行排序，然后输入以下数值，在应用前设置一个过滤器，突出显示匹配的基因簇。

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/hi-search-pane-02.png)

按逆时针顺序排列的第一个基因簇是与所列标准最匹配的一个。经过仔细检查：

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/hi-search-pane-03.png)

人们可以看到，尽管基因组中的序列具有几何上的同质性，但在各基因组中排列的残基之间存在着巨大的功能变化（这里只显示了一部分排列）：

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/hi-search-pane-03-inspect.png)

那些读过我们关于这个[主题研究](https://peerj.com/articles/4320/)的人，也许不会惊讶地知道，这个特定基因簇的COG功能注释解析为一种与细胞壁/膜/包膜生物形成有关的[酶](https://en.wikipedia.org/wiki/N-acetylmuramoyl-L-alanine_amidase)。当事情被证实时，总是很好。

`审视系统基因组学`：这里是同质性指数的另一个使用例子。我们经常使用单拷贝核心基因簇进行系统发育分析，以估计我们基因组之间的进化关系。识别单拷贝核心基因簇很容易，要么通过高级过滤器，要么通过人工对基因簇进行分箱。

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/hi-core-01.png)

但是单拷贝核心基因簇将包含许多排列不整齐的基因簇，你可能不想将其用于系统发育分析，以便将源于生物信息学决定在何处放置缺口的噪声影响降到最低。另一方面，在这个集合中会有许多基因簇是近乎相同的，这对于推断系统发育关系是相当无用的。幸运的是，你可以使用同质性指数和高级搜索选项来识别那些在几何上完美，但在功能上多样的基因：

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/hi-core-02.png)

你可以很容易地将那些符合这些标准的追加到一个单独分箱：

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/hi-core-03.png)

并进行快速分析，看看他们会如何直接在界面上组织你的基因组：

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/hi-core-04.png)

或者你可以得到这些基因簇的FASTA文件，其中有对齐和串联的氨基酸序列，以做更合适的系统发育分析：

```bash
$ anvi-get-sequences-for-gene-clusters -p PROCHLORO/Prochlorococcus_Pan-PAN.db \
                                       -g PROCHLORO-GENOMES.db \
                                       -C default -b Better_core \
                                       --concatenate-gene-clusters \
                                       -o better_core.fa
```

不用说，每个基因簇的同质性指数估计值也会出现在`anvi-summarize`的摘要文件中，以满足统计需求。

#### 在泛基因组中了解功能的意义

一旦有了泛基因组，我们通常想做的关键事情之一是看一下与我们的基因簇相关的功能。这是一个关键而又复杂的挑战，我们可以通过多种方式来解决。在这里，我们将介绍如何识别富集于你的泛基因组中的一些支系或亚支系的功能。此外，我们还将讨论如何找到泛基因组的功能核心。这是通过我们新改进的`anvi-get-enriched-functions-per-pan-group`程序完成的。

这个程序利用你的泛数据库的图层附加数据表中的信息来识别你的基因组中的 "组"，并找到在这些组中富集的功能，即这些基因组所特有的功能，而在这个组以外的基因组中主要是没有的。要使用这个功能，你必须至少有一个分类的附加层信息（可以很容易地通过`anvi-import-misc-data`完成），并且你的基因组存储至少有一个功能注释源（如果你运行`anvi-gen-genomes-storage`时使用的每个重叠群数据库都有相同的功能注释源，这将自动成为一种情况）。

> *Alon关于anvi'o功能丰富度分析的简短 "幕后 "讲座，供好奇者参考*：
>
> 对于那些喜欢深入了解细节的人，这里有一些幕后信息。
>
> 为了使这一分析与其他一切与泛基因组有关的东西兼容，我们决定，它应该集中在基因簇上，因为它们是我们泛基因组的核心。这意味着功能分析的第一步是尝试将每个基因簇与一个功能联系起来。这是必要的，因为基因簇默认没有功能注释，因为功能注释在anvi'o中是在单个基因的水平上完成的。
>
> 在理想情况下，一个基因簇中的所有基因都会被注释为相同的功能。虽然在现实中通常是这样，但这并不总是真的。在一个基因簇有多种功能的情况下，我们选择最常见的功能，即基因簇中最多的基因匹配的功能（如果有多种功能并列，那么我们就任意选择一种）。如果该基因簇中没有一个基因被注释，那么该基因簇就没有与之相关的功能。
>
> 当然，当我们将每个基因簇与一个功能相关联时，我们最终可能在一个泛基因组中出现多个具有相同功能的基因簇。根据我们的经验，大多数功能都与一个基因簇相关联，但仍有很多功能与多个基因簇相关联，这在含有远缘基因组的泛基因组中会更常见。在这些情况下，为了找到某个功能在基因组中的出现率，我们只需“合并”与该功能相关的所有基因簇的出现率（对于诸位这些计算型的读者来说，我们只是简单地取基因簇在各基因组中的出现频率向量之和）。
>
> 细心的读者会注意到，我们在下面的文字中对`功能注释`和`功能关联`进行了区分。当我们提到`功能注释`时，我们指的是功能注释源（即COG、EggNOG等）对单个基因的功能注释，而基因簇的`功能关联`是指基因簇与上述单个功能的关联。
>
> 好了，现在我们有了一个基因组中功能的频率表，我们用它来作为功能丰富度测试的输入。这个测试是由[Amy Willis](https://github.com/adw96)在`R`语言中实现的（你可以在[这里](https://github.com/merenlab/anvio/blob/master/sandbox/anvi-script-enrichment-stats)找到这个脚本），它使用通用线性模型和`logit linkage`函数来计算每个功能的富集分数和p值。使用软件包`qvalue`对p值进行假检测率校正，以考虑到多次测试。
>
> 除了丰富性测试，我们还使用一个简单的启发式方法来寻找与每个功能相关联的群体。**这种关联只对那些真正丰富的功能有意义，否则应该被忽略。**我们简单地确定，对于每一个功能，相关的组是指该功能在基因组中的出现率大于正态分布下的预期出现率（即如果该功能在所有组的基因组中出现的概率相同）。从数学上讲，如果我们把$E_{ij}$表示为空分布下第$i$组的预期基因组数，其函数为$j$，我们认为空分布是一个均匀分布。因此：
> $$
> \begin{equation}\label{eq:expected_occurrence}
>  E_{ij} = \frac{n_i}{\sum_{i'=1}^N n_{i'}} \cdot \sum_{i'=1}^N O_{i'j}
> \end{equation}
> $$
>
> 而我们把第$i$组中实际出现的函数$j$表示为$O_{ij}$，那么我们认为相关组是$O_{ij} > E_{ij}$的组。现在我们可以使用所有这些信息来探索我们的数据，请看下面的细节。

让我们用原绿球藻的例子看看能用它做什么。首先，我们将比较低光照与高光照基因组，以便利用`light`分类附加层数据（如果这对你来说没有意义，请回到上面的一个泛基因组数字，看看附加层数据`light`），看看是否有任何功能是这两组独有的。

```bash
$ anvi-get-enriched-functions-per-pan-group -p PROCHLORO/Prochlorococcus_Pan-PAN.db \
  -g PROCHLORO-GENOMES.db \
  --category light \
  --annotation-source COG_FUNCTION \
  -o PROCHLORO-PAN-enriched-functions-light.txt \
  --functional-occurrence-table-output PROCHLORO-functions-occurrence-frequency.txt
```

> 除了功能丰富的输出`PROCHLORO-PAN-enriched-functions-light.txt`之外，我们还生成了一个额外的（可选）输出`PROCHLORO-functions-occurrence-frequency.txt`。我们在下面讨论如何用函数做一个快速的泛基因组时，会更多地讨论这个输出。

下面是输出文件`PROCHLORO-PAN-enriched-functions-light.txt`的结构（有更多的列，向右滚动可以看到）。

| COG_FUNCTION                                                 | enrichment_score | unadjusted_p_value | adjusted_q_value | associated_groups | function_accession | gene_clusters_ids                                  | p_LL | p_HL | N_LL | N_HL |
| ------------------------------------------------------------ | ---------------- | ------------------ | ---------------- | ----------------- | ------------------ | -------------------------------------------------- | ---- | ---- | ---- | ---- |
| Proteasome lid subunit RPN8/RPN11, contains Jab1/MPN domain metalloenzyme (JAMM) motif | 31.00002279      | 2.58E-08           | 1.43E-06         | LL                | COG1310            | GC_00002219, GC_00003850, GC_00004483              | 1    | 0    | 11   | 20   |
| Adenine-specific DNA glycosylase, acts on AG and A-oxoG pairs | 31.00002279      | 2.58E-08           | 1.43E-06         | LL                | COG1194            | GC_00001711                                        | 1    | 0    | 11   | 20   |
| Periplasmic beta-glucosidase and related glycosidases        | 31.00002279      | 2.58E-08           | 1.43E-06         | LL                | COG1472            | GC_00002086, GC_00003909                           | 1    | 0    | 11   | 20   |
| Single-stranded DNA-specific exonuclease, DHH superfamily, may be involved in archaeal DNA replication intiation | 31.00002279      | 2.58E-08           | 1.43E-06         | LL                | COG0608            | GC_00002752, GC_00003786, GC_00004838, GC_00007241 | 1    | 0    | 11   | 20   |
| Ser/Thr protein kinase RdoA involved in Cpx stress response, MazF antagonist | 31.00002279      | 2.58E-08           | 1.43E-06         | LL                | COG2334            | GC_00002783, GC_00003936, GC_00004631, GC_00005468 | 1    | 0    | 11   | 20   |
| (…)                                                          | (…)              | (…)                | (…)              | (…)               | (…)                | (…)                                                | (…)  | (…)  | (…)  | (…)  |
| Signal transduction histidine kinase                         | -7.34E-41        | 1                  | 1                | NA                | COG5002            | GC_00000773, GC_00004293                           | 1    | 1    | 11   | 20   |
| tRNA A37 methylthiotransferase MiaB                          | -7.34E-41        | 1                  | 1                | NA                | COG0621            | GC_00000180, GC_00000851                           | 1    | 1    | 11   | 20   |

以下是对每一栏的描述：

1. **category类别**是你从图层附加数据表中选择的列，以便在你的基因组中分辨组别。在原绿球藻的案例中，我们有两个光照组：低光照（LL），和高光照（HL）。输出的表格首先根据这一栏进行排序，在每个组内，表格根据富集度得分进行排序。
2. **COG_FUNCTION**这一栏是计算富集度的具体功能的名称。在这个例子中，我们选择使用`COG_FUNCTION`进行功能注释，因此列的标题是`COG_FUNCTION`。你可以使用`--annotation-source`指定你的泛数据库中的任何一个功能注释源，然后分析就会根据这个注释源来进行。即使你的基因组存储中有多个功能注释源，在这个程序的一次运行中也只能使用一个源。如果你愿意，你可以多次运行它，每次使用不同的注释源。如果你不记得你的基因组存储中哪些注释源是可用的，你可以使用`–list-annotation-sources`。
3. **enrichment_score**是一个分数，用来衡量这个功能对属于特定组的基因组与你的泛基因组中所有其他基因组的独特程度。这个分数是由[Amy Willis](https://github.com/adw96)开发的。关于我们如何产生这个分数的更多细节，请看下面Amy的说明。
4. **unadjusted_p_value**是充实度检验的p值（未对多重检验进行调整）。
5. **adjusted_q_value**是调整后的q值，用于控制多次测试导致的假检测率（FDR）（这是必要的，因为我们是单独运行富集测试的每个函数）。
6. **associated_groups**是你的分类数据中与该函数相关的组（或标签）的列表。请注意，如果丰富度分数很低，那么这就没有意义（如果函数没有被丰富，那么它就没有真正与任何特定的组相关联）。请看上面Alon的解释，了解这些是如何计算出来的。
7. **function_accession**是函数的登录号。
8. **gene_clusters_ids**是与该函数相关的基因簇。注意，每个基因簇将与一个函数相关，但一个函数可以与多个基因簇相关。
9. **p_LL**和**p_HL**对于每个组（在这个例子中，有两个组：LL和LH），将有一列是我们检测到功能的组成员的部分。
10. **N_LL**和**N_HL**对于每个组来说，这些列都指定了该组的基因组的总数。

> 此实例只包括两个类别（LL和HL），可以根据需求拥有多个不同类别。只要记住，若某些组中的基因组数量很少，则统计测试结果不会很可靠。要使测试结果可靠，每组中最小基因组数取决于许多因素，但若任意一组的基因组少于8个，建议谨慎进行。

> Amy Willis关于功能丰富度分数的说明：
>
> 这里提出并在Anvi’o中实现的功能丰富度分数和Rao检验统计的一样。基本上，它把每个类别（这里是高光和弱光）作为逻辑回归（二项式 GLM（[广义线性模型](https://blog.csdn.net/gactyxc/article/details/52488598)））中的一个解释变量，并测试分类变量在解释功能发生方面的意义。该测试考虑了这样一个事实，即从一个类别中观察到的基因组可能比另一个类别多。像往常一样，有更多的基因组使测试更加可靠。有很多不同的方法来做这个测试，但我们做了一些调查，发现在所有控制第一类错误率的测试中，拉奥测试的力量最高。由于许多用户会关注对许多功能的富集测试，默认情况下，我们通过控制错误发现率来调整多重测试。因此，如果你使用`anvi-get-enriched-functions-per-pan-group`，请在你的论文中报告q值而不是p值。

现在让我们搜索一下表中的一个顶级功能 "Ser/Thr protein kinase RdoA involved in Cpx stress response, MazF antagonist（参与Cpx应激反应的Ser/Thr蛋白激酶RdoA，MazF拮抗剂）"，它富含LL组的成员，我们可以在表中看到，它与四个基因簇相匹配。

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/ser_thr_kinase_gene_clusters.png)

事实上，如果我们仔细观察，能发现这个功能与一个基因簇相匹配，而这个基因簇对于四个弱光族中的每一个都是独一无二的，是泛基因组中弱光基因组的单拷贝核心基因。

来看看另一个富集的功能：`Exonuclease VII, large subunit`（外切酶VII，大亚单位）。当搜索这个功能时，应该小心，因为这个功能的名称包含一个逗号，而交互式界面中的功能搜索选项将逗号视为分隔多个要同时搜索的功能。因此，我刚刚搜索了`Exonuclease VII`，下面是搜索结果：

<img src="https://merenlab.org/images/anvio/2016-11-08-pan-genomics/Exonuclease-VII.png" style="zoom: 33%;" />

我们可以看到，该搜索与外切酶VII、大亚基和小亚基的命中率都相匹配，共有22个命中。

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/Exonuclease-VII-2.png)

大亚基与在`CORE LL`中的一个基因簇相匹配，而小亚基则与每个族特定核心中的一个基因簇相匹配（类似于我们在上面看到的Ser/Thr蛋白激酶的情况）。这两个基因也是弱光成员特有的单拷贝核心的一部分，强光成员没有。

（1）利用功能创建快速泛基因组

下一步介绍另外的特征`--functional-occurrence-table-output`，我们的命令行包含此参数。

```bash
$ anvi-get-enriched-functions-per-pan-group -p PROCHLORO/Prochlorococcus_Pan-PAN.db \
  -g PROCHLORO-GENOMES.db \
  --category light \
  --annotation-source COG_FUNCTION \
  -o PROCHLORO-PAN-enriched-functions-light.txt \
  --functional-occurrence-table-output PROCHLORO-functions-occurrence-frequency.txt
```

该可选输出是TAB制表符分隔文件，其具有基因组中功能的发生信息的频率（即基因组中的许多基因与每个功能有关）。

 `PROCHLORO-PAN-enriched-functions-clade.txt`看起来这样：

`PROCHLORO-functions-occurrence-frequency.txt`看起来这样：

|                                                              | AS9601 | CCMP1375 | EQPAC1 | GP2  | LG   | MED4 | MIT9107 | MIT9116 | MIT9123 | MIT9201 | MIT9202 | MIT9211 | MIT9215 | MIT9301 | MIT9302 | MIT9303 | MIT9311 | MIT9312 | MIT9313 | MIT9314 | MIT9321 | MIT9322 | MIT9401 | MIT9515 | NATL1A | NATL2A | PAC1 | SB   | SS2  | SS35 | SS51 |
| ------------------------------------------------------------ | ------ | -------- | ------ | ---- | ---- | ---- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------ | ------ | ---- | ---- | ---- | ---- | ---- |
| 3-deoxy-D-manno-octulosonate 8-phosphate phosphatase KdsC and related HAD superfamily phosphatases | 0      | 0        | 0      | 0    | 0    | 0    | 0       | 0       | 0       | 0       | 0       | 0       | 0       | 0       | 0       | 1       | 0       | 0       | 1       | 0       | 0       | 0       | 0       | 0       | 0      | 0      | 0    | 0    | 0    | 0    | 0    |
| Creatinine amidohydrolase/Fe(II)-dependent formamide hydrolase involved in riboflavin and F420 biosynthesis | 1      | 1        | 1      | 1    | 1    | 1    | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1      | 1      | 1    | 1    | 1    | 1    | 1    |
| RNA recognition motif (RRM) domain                           | 1      | 1        | 1      | 1    | 1    | 1    | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1       | 1      | 1      | 1    | 1    | 1    | 1    | 1    |
| (…)                                                          | (…)    | (…)      | (…)    | (…)  | (…)  | (…)  | (…)     | (…)     | (…)     | (…)     | (…)     | (…)     |         |         |         |         |         |         |         |         |         |         |         |         |        |        |      |      |      |      |      |

使用功能发生表进行可视化。首先，修正功能的名称，去掉逗号等东西。基本上，我们只保留字母、数字和字符，并将任何非字母、非数字字符的序列替换为一个`_`。

使用脚本：

```bash
$ wget https://gist.githubusercontent.com/ShaiberAlon/aff0b2493637a370c7d52e1a5aacecea/raw/f088d6af4b4b26afe43c67874e2563c407039355/fix_functional_occurrence_table.py
```

使用方法：

```bash
$ python fix_functional_occurrence_table.py \
         --input-file PROCHLORO-functions-occurrence-frequency.txt \
         --output-file PROCHLORO-functions-occurrence-frequency-fixed.txt \
         --name-dict-output PROCHLORO-functions-names-dict.txt
```

检查名称的变化是否产生了多余的名称：

```bash
$ cut -f 2 PROCHLORO-functions-names-dict.txt | sort | uniq -d
```

可以看到`Fatty_acid_desaturase`和`Protein_tyrosine_phosphatase`。这是因为有两个`COG`功能`Protein-tyrosine phosphatase`（登录号`COG2453`）和`Protein-tyrosine-phosphatase`（登录号`COG0394`）在泛基因组中匹配不同的基因簇。因为我们不能创建一个有重复节点的树，因为我们不能真的说这些是不同的功能，在上面的脚本中，除了改变名称之外，它还将这些重复出现的情况合并。（使用逻辑或`or`合并它们的发生）

然后我们在交互式界面中创建了树：

```bash
$ anvi-matrix-to-newick PROCHLORO-functions-occurrence-frequency-fixed.txt \
                        -o PROCHLORO-functions-tree.txt
$ anvi-matrix-to-newick PROCHLORO-functions-occurrence-frequency-fixed.txt \
                        -o PROCHLORO-functions-layers-tree.txt \
                        --transpose
```

我们进行快速模拟运行，创建一个手动模式的配置文件数据库。

```bash
$ anvi-interactive -p PROCHLORO-functions-manual-profile.db \
                   --tree PROCHLORO-functions-tree.txt \
                   -d PROCHLORO-functions-occurrence-frequency-fixed.txt \
                   --manual \
                   --dry-run
```

为图层顺序导入树：

```bash
$ echo -e "item_name\tdata_type\tdata_value" > PROCHLORO-functions-layers-order.txt
$ echo -e "PROCHLORO_functions_tree\tnewick\t`cat PROCHLORO-functions-layers-tree.txt`" \
                             >> PROCHLORO-functions-layers-order.txt
$ anvi-import-misc-data PROCHLORO-functions-layers-order.txt \
                        -p PROCHLORO-functions-manual-profile.db \
                        -t layer_orders \
                        --just-do-it
```

我们可以从泛数据库中获得一些关于基因组的信息

```bash
$ anvi-export-misc-data -p PROCHLORO/Prochlorococcus_Pan-PAN.db \
                        -t layers \
                        -o PROCHLORO-layer-additional-data.txt
```

然后将其导入我们的手动模式配置文件数据库中：

```bash
$ anvi-import-misc-data PROCHLORO-layer-additional-data.txt \
                        -p PROCHLORO-functions-manual-profile.db \
                        -t layers
```

你下载的工作目录包括一个漂亮的状态，我们为这个配置文件数据库创建了一个集合，让我们导入这些：

```bash
$ anvi-import-state -p PROCHLORO-functions-manual-profile.db \
                    -s PROCHLORO-manual-default-state.json \
                    -n default
```

可以使用这个临时脚本来获得核心功能。你可以下载该脚本：

```bash
$ wget https://gist.githubusercontent.com/ShaiberAlon/2a8c1b12a372c77a7569dec7c317d37b/raw/55603505c2d1d40ce0528671e25e9f5c82b4bf43/get-core-functions.py
```

使用方法：

```bash
$ python get-core-functions.py \
         --input PROCHLORO-functions-occurrence-frequency-fixed.txt \
         --output PROCHLORO-functions-collection.txt
```

现在我们可以导入这些集合：

```bash
# let's first create a collection info file so ew can all have the same colors in the interactive :-)
$ echo -e "Functional_core\tUNKOWN\t#8c0735" > PROCHLORO-functions-collection-info.txt
$ anvi-import-collection -p PROCHLORO-functions-manual-profile.db \
                         -C default \
                         PROCHLORO-functions-collection.txt \
                         --bins-info PROCHLORO-functions-collection-info.txt
```

可视化：

```bash
$ anvi-interactive -p PROCHLORO-functions-manual-profile.db \
                   -t PROCHLORO-functions-tree.txt \
                   -d PROCHLORO-functions-occurrence-frequency-fixed.txt \
                   --title "Prochlorococcus Pan - functional occurrence" \
                   --manual
```

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/Functional-frequency.png)

我们可以看到，功能的出现几乎完美地复现了所有四个`LL`支系。相比之下，两个`HL`支系似乎稍微混在一起。

我们有一个869个核心功能的集合。但核心功能有点分散，这是由于我们使用了功能的出现频率。让我们根据发生率（即1和0）来增加一个组织。为了做到这一点，我们首先使用这个临时脚本转换频率表。你可以先下载它：

```bash
$ wget https://gist.githubusercontent.com/ShaiberAlon/8ebd5fb43308086d5455bea18bbdefee/raw/1e83080ac17244a68f0d2a2f25402ee8c0180634/convert-frequencey-table-to-occurrence-table.py
```

使用方法：

```bash
$ python convert-frequencey-table-to-occurrence-table.py \
         --input PROCHLORO-functions-occurrence-frequency-fixed.txt \
         --output PROCHLORO-functions-occurrence-fixed.txt
```

我们可以生成一个项目顺序和图层顺序树：

```bash
$ anvi-matrix-to-newick PROCHLORO-functions-occurrence-fixed.txt \
                        -o PROCHLORO-functions-occurrence-tree.txt

$ anvi-matrix-to-newick PROCHLORO-functions-occurrence-fixed.txt \
                        -o PROCHLORO-functions-occurrence-layers-tree.txt \
                        --transpose
```

我们导入新的图层顺序：

```bash
$ echo -e "PROCHLORO_functions_occurrence_tree\tnewick\t`cat PROCHLORO-functions-occurrence-layers-tree.txt`" \
                             >> PROCHLORO-functions-layers-order.txt

$ anvi-import-misc-data PROCHLORO-functions-layers-order.txt \
                        -p PROCHLORO-functions-manual-profile.db \
                        -t layer_orders \
                        --just-do-it
```

再一次可视化：

```bash
$ anvi-interactive -p PROCHLORO-functions-manual-profile.db \
                   -t PROCHLORO-functions-occurrence-tree.txt \
                   -d PROCHLORO-functions-occurrence-frequency-fixed.txt \
                   --title "Prochlorococcus Pan - functional occurrence" \
                   --manual
```

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/Functional-occurrence.png)

现在所有的核心功能都聚集在一起了。我们还可以使用我们用二进制发生数据生成的树来改变层的顺序（只需在图层标签中选择`PROCHLORO_functions_occurrence_tree`即可）：

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/Functional-occurrence_2.png)

当我们使用二进制发生数据时，那么我们就会看到四个`LL`支系是完美复现的，但`HL`支系是真正的混合。

让我们来看看核心功能是如何对应于基因簇的。将使用一个临时的小脚本，你可以下载:

```bash
$ wget https://gist.githubusercontent.com/ShaiberAlon/d2adc8a55a2ac1ea6458d67e90181a7e/raw/3ad0efbf93038e627f2a4aa268b5f3a8beb99fa9/get-gcs-of-core-functions.py
```

使用方法：

```bash
$ python get-gcs-of-core-functions.py \
         --enrichment-data PROCHLORO-PAN-enriched-functions-light.txt \
         --core-functions PROCHLORO-functions-collection.txt \
         --name-dict PROCHLORO-functions-names-dict.txt \
         --output-file PROCHLORO-GCs-of-core_functions.txt
```

然后我们得到一个有2613个基因簇的文件。现在我们可以将其与我们上面的基因簇集合进行比较。例如，我们可以发现，在`CORE_LL`中的基因簇有多少是在所有31个原绿球藻基因组的功能核心中。

因此，让我们假设之前做了这些选择，现在可以导出`GC`的集合。

```bash
$ anvi-export-collection -p PROCHLORO/Prochlorococcus_Pan-PAN.db \
                         -C default \
                         -O PROCHLORO-PAN-default-collection
```

```bash
$ for gc in `grep CORE_LL PROCHLORO-PAN-default-collection.txt`
> do
>     grep $gc PROCHLORO-GCs-of-core_functions.txt
> done > CORE_LL_included_in_functional_core.txt
```

我们发现，144个基因簇中有103个是功能核心的一部分。而对于`HL`来说，499个中有294个被发现是功能核心的一部分。需要记住的一件事是，没有功能关联的基因簇不包括在这个分析中。

我们可以找到所有与功能相关的基因簇：

```bash
$ awk -F $'\t' '{ print $7 }' PROCHLORO-PAN-enriched-functions-light.txt |
    tr ',' '\n' |
      sed 's/ //g' > all_gene_clusters_with_functions.txt
```

有3629个具有功能的基因簇。有多少属于`CORE_HL`的基因簇有功能？

```bash
$ for gc in `grep CORE_HL PROCHLORO-PAN-default-collection.txt`
> do
>     grep $gc all_gene_clusters_with_functions.txt;
> done > HL_CORE_GC_with_functions.txt

$ wc -l HL_CORE_GC_with_functions.txt
321
```

在`CORE_HL`中，有321个（总共499个）基因簇有功能。因此，`CORE_HL`中的许多基因簇没有被发现是功能核心的一部分，只是没有任何功能注释。

#### 计算基因组的平均核苷酸相似度（以及其他基因组相似性指标！）。

Anvi'o还包含一个`anvi-compute-ani`（原名为`anvi-compute-genome-similarity`）程序，使用各种相似性指标，如[PyANI](https://doi.org/10.1039/C5AY02550H)来计算你的基因组的平均核苷酸相似度，[sourmash](https://doi.org/10.21105/joss.00027)来计算你的基因组的最小哈希（MinHash）距离。它期待外部基因组文件、内部基因组文件或指向FASTA文件路径的fasta文本文件的任何组合（每个FASTA被假定为1个基因组）。此外，`anvi-compute-genome-similarity`还可以选择接受一个泛数据库，将所有的结果作为附加层数据加入其中。

还是原绿球藻泛基因组案例：

```bash
$ anvi-compute-genome-similarity --external-genomes external-genomes.txt \
                                 --program pyANI \
                                 --output-dir ANI \
                                 --num-threads 6 \
                                 --pan-db PROCHLORO/Prochlorococcus_Pan-PAN.db
```

一旦完成，我们可以再次对泛基因组进行可视化，看看有什么新玩意：

```bash
$ anvi-display-pan -g PROCHLORO-GENOMES.db \
                   -p PROCHLORO/Prochlorococcus_Pan-PAN.db
```

当第一眼看到它时，不会看到任何不寻常的东西。但如果进入**"Layers图层"**选项卡，会看到下面的补充：

<img src="https://merenlab.org/images/anvio/2016-11-08-pan-genomics/layer-groups-ani.png" style="zoom:50%;" />

如果点击复选框，例如`ANI_percentage_identity`，你会看到一组新的条目将被添加到图层数据条目列表中。然后，如果你点击**"Draw绘制"**或**"Redraw layer data重绘图层数据"**按钮，你应该看到`ANI`被添加到你的显示中：

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/prochlorococcus-ani.png)

> **一个如何排序基因组的小笔记：**
>
> 对我来说，如何在基因簇方面对基因组进行排序一直是一个问号。是否应该使用基因簇的存在/不存在模式来组织基因组（在这种情况下，人们忽略了旁系物，并使用二进制表格来对基因组进行分类）？还是应该依靠基因簇频率数据来排序（在这种情况下，人们确实考虑了旁系物，所以他们的表格不再是二进制的，而是包含每个基因簇中每个基因组的基因数的频率）？
>
> 感谢Özcan对代码库的[新补充](https://github.com/merenlab/anvio/commit/aa007cf902dea2de4bd63524cd49f0566cf2511d)，当我在编写本节教程时，对“如何在泛基因组中排列基因组”这个问题有了一个意外的观察。
>
> 这就是我根据基因簇频率数据对原绿球藻基因组进行排序时，ANI矩阵的样子：
>
> ![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/ani-gc-freqs.png)
>
> 相比之下，当我根据基因簇存在/不存在的数据对基因组进行排序时，ANI矩阵是这样的：
>
> ![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/ani-gc-preabs.png)
>
> 如果你正在处理分离的基因组，也许你应该考虑根据基因簇的频率来排序，因为你会期望基于基因簇的基因组的适当组织往往应该与它们的整体相似性相匹配。这里有一些小的说明：
>
> - 在这种情况下，我们很容易看到，通过基因簇存在/不存在的数据来组织基因组的工作做得很差，把高光II组（紫色）和高光I组（便便色）的基因组混在一起。我们可以清楚地识别这个问题，因为我们知道这些基因组所属的支系，在你不知道这些关系的情况下，似乎基因簇频率可以更准确地组织你的基因组。
> - 令人难过的是，MAG经常会缺乏多拷贝基因，而且它们的旁系亲属较少（因为短读数的组装会产生非常复杂的德布莱英图（[De Bruijn Graph](https://zhuanlan.zhihu.com/p/57177938)），它抹去了特定基因组中的所有冗余），因此它们的适当组织不会真正受益于基因簇频率数据，至少不会像隔离基因组那样，我们在基于基因簇存在/不存在数据的组织中看到的错误会对我们的庞然大物产生较大影响。
> - 看到高光组II中出现的那些亚支系了吗？如果你有兴趣，请看看我们关于[宏泛基因组的论文](https://peerj.com/articles/4320/)（特别是**“The metapangenome reveals closely related isolates with different levels of fitness”**一节），其中我们将HL-II分为多个亚族，并表明尽管这些基因组之间的差异很小，但这些亚族显示了明显不同的环境分布模式。在该研究中，我们可以根据基因簇频率和环境分布模式定义的亚支系与ANI所揭示的群体相当吻合。这又回到了微生物学中一些最基本的问题，即如何定义微生物生命的生态相关单位。我不知道我们是否接近做出任何定义，但我可以告诉你，我们正在使用的那些“系统发育标志物”......我不确定它们是否真的那么有效（笑）。

#### 统计Anvi’o泛基因组

当你把选择的基因簇存储为一个集合时，anvi'o将允许你对这些结果进行统计：

> 即使你想简单地统计泛基因组中的一切，而不在界面中做任何选择，你仍然需要在泛数据库中建立一个集合。但幸运的是，你可以使用程序`anvi-script-add-default-collection`来添加一个包含每个基因簇的默认集合。

该统计步骤给了你两个重要的东西：一个静态的HTML网页，你可以压缩并与你的同事分享，或者作为补充数据文件添加到你的出版物中，以及在输出目录中的一个全面的TAB制表符分隔文件，描述每个基因簇。

你可以用`anvi-summarize`程序来统计一个集合，这个命令的通用形式看起来像这样：

```bash
$ anvi-summarize -p PROJECT-PAN.db \
                 -g PROJECT-PAN-GENOMES.db \
                 -C COLLECTION_NAME \
                 -o PROJECT-SUMMARY
```

如果你打开统计目录下的`index.html`文件，你会看到一个输出，其中有关于分析的一些基本信息：

<img src="https://merenlab.org/images/anvio/2016-11-08-pan-genomics/summary.png" style="zoom: 15%;" />

以及基因簇的TAB制表符分隔文件：

![](https://merenlab.org/images/anvio/2016-11-08-pan-genomics/summary-file.png)

这个文件的结构将是这样的，它将给你一个机会以更详细的方式审查你的基因簇（你可能需要向右滚动以看到更多的表格）：

| unique_id | gene_cluster_id | bin_name | genome_name | gene_callers_id | COG_FUNCTION_ACC |                   COG_FUNCTION                    | COG_CATEGORY_ACC |                  COG_CATEGORY                   |       aa_sequence       |
| :-------: | :-------------: | :------: | :---------: | :-------------: | :--------------: | :-----------------------------------------------: | :--------------: | :---------------------------------------------: | :---------------------: |
|     1     |   PC_00001990   |          |   MIT9303   |      30298      |     COG1199      |             Rad3-related DNA helicase             |        L         |      Replication, recombination and repair      | MLEARSHQQLKHLLLQNSSP(…) |
|    (…)    |       (…)       |   (…)    |     (…)     |       (…)       |       (…)        |                        (…)                        |       (…)        |                       (…)                       |           (…)           |
|    91     |   PC_00001434   | Core_HL  |   MIT9322   |      42504      |     COG3769      | Predicted mannosyl-3-phosphoglycerate phosphatase |        G         |      Carbohydrate transport and metabolism      | MIENSSIWVVSDVDGTLMDH(…) |
|    (…)    |       (…)       |   (…)    |     (…)     |       (…)       |       (…)        |                        (…)                        |       (…)        |                       (…)                       |           (…)           |
|    257    |   PC_00000645   | Core_all |   MIT9322   |      42217      |     COG1185      |     Polyribonucleotide nucleotidyltransferase     |        J         | Translation, ribosomal structure and biogenesis | MEGQNKSITFDGREIRLTTG(…) |
|    (…)    |       (…)       |   (…)    |     (…)     |       (…)       |       (…)        |                        (…)                        |       (…)        |                       (…)                       |           (…)           |
|   2019    |   PC_00001754   | Core_LL  |   NATL2A    |      49129      |     COG0127      |  Inosine/xanthosine triphosphate pyrophosphatase  |        F         |       Nucleotide transport and metabolism       | MDNVPLVIASGNKGKIGEFK(…) |
|    (…)    |       (…)       |   (…)    |     (…)     |       (…)       |       (…)        |                        (…)                        |       (…)        |                       (…)                       |           (…)           |
|   5046    |   PC_00001653   |          |    PAC1     |      52600      |     COG1087      |              UDP-glucose 4-epimerase              |        M         |     Cell wall/membrane/envelope biogenesis      | MRVLLTGGAGFIGSHIALLL(…) |
|   5047    |   PC_00001653   |          |     LG      |      7488       |     COG1087      |              UDP-glucose 4-epimerase              |        M         |     Cell wall/membrane/envelope biogenesis      | MNRILVTGGAGFIGSHTCIT(…) |
|   5048    |   PC_00001653   |          |    SS35     |      56661      |     COG1087      |              UDP-glucose 4-epimerase              |        M         |     Cell wall/membrane/envelope biogenesis      | MNRILVTGGAGFIGSHTCIT(…) |
|   5049    |   PC_00001653   |          |   NATL2A    |      49604      |     COG1087      |              UDP-glucose 4-epimerase              |        M         |     Cell wall/membrane/envelope biogenesis      | MRVLLTGGSGFIGSHVALLL(…) |
|    (…)    |       (…)       |   (…)    |     (…)     |       (…)       |       (…)        |                        (…)                        |       (…)        |                       (…)                       |           (…)           |

这个文件将把每个基因组中的每个基因与你通过界面或通过`anvi-import-collection`程序进行命名的每个选择联系起来，还可以让你获得每个基因的氨基酸序列和功能。

## 参考链接

1. [All programs and scripts in anvi’o](https://merenlab.org/software/anvio/vignette/)
2. [All anvi'o programs and artifacts](https://merenlab.org/software/anvio/help/7/)
3. [Infant Gut](https://merenlab.org/tutorials/infant-gut/)
4. [Anvi'o User Tutorial for Metagenomic Workflow](https://merenlab.org/2016/06/22/anvio-tutorial-v2/)
5. [Working with BAM Files](https://www.ncbi.nlm.nih.gov/tools/gbench/install/)
6. [三天实现独立分析宏基因组数据(有参、无参和分箱等)](https://blog.csdn.net/woodcorpse/article/details/106553640)
7. [Binning without mapping](https://merenlab.org/2016/06/06/working-with-contigs-only/)
8. [Binning without mapping · Issue #226 · merenlab/anvio](https://github.com/merenlab/anvio/issues/226)
9. [An anvi’o workflow for microbial pangenomics](https://merenlab.org/2016/11/08/pangenomics-v2/)
10. [使用anvi'o 进行微生物pangenomics泛基因组分析](https://www.jianshu.com/p/b48845851a20)
11. [宏基因组实战9. 组装assembly和分箱bin结果可视化—Anvi'o](https://mp.weixin.qq.com/s?__biz=MzUzMjA4Njc1MA==&mid=2247484522&idx=1&sn=d8aba1e86d6dddf5f6c593206b16b0c7&scene=21#wechat_redirect)
12. [anvi'server - An open source interactive visualization platfrom](https://anvi-server.org/)
13. [Prochlorococcus Metapangenome](https://anvi-server.org/merenlab/prochlorococcus_metapangenome)
14. [The anvi'o interactive interface](https://merenlab.org/2016/02/27/the-anvio-interactive-interface/)
15. [A tutorial on the anvi'o interactive interface](https://merenlab.org/tutorials/interactive-interface/)
16. [Notes on genome refinement with anvi'o](https://merenlab.org/2017/05/11/anvi-refine-by-veronika/)
17. [DeepL翻译：全世界最准确的翻译](https://www.deepl.com/)
18. [Word中的SVG格式的矢量插图问题](https://blog.csdn.net/shaoyubin999/article/details/79450168)
19. [Linux下bowtie2安装(非conda)和配置](https://www.jianshu.com/p/7e8b1e743e3d)
20. [samtools的安装和使用](https://www.jianshu.com/p/6b7a442d293f)

