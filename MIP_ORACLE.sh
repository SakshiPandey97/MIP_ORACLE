#!/bin/bash

helpFunction()
{
   echo "NOTE: The FASTA definition line should match the CARD database format. Ex.>gb|EU555534|+|0-882|ARO:3002316|KPC-6 [Klebsiella pneumoniae]"
   echo "Usage: $0 -i 'KPC' -o 'KPC_final_results' -l codes/ncbi-blas -j '/DATA/databases/blast/nt'"
   echo -e "\t-i Name of the input FASTA file(There's no need to add the file extension)"
   echo -e "\t-o Name of the ouptut file(There's no need to add the file extension)"
   echo -e "\t-l The location of the BLAST module"
   echo -e "\t-j The location of the nt BLAST database"
   exit 1 # Exit script after printing help
}

while getopts "i:o:l:j:" opt
do
   case "$opt" in
      i ) parameterI="$OPTARG" ;;
      o ) parameterO="$OPTARG" ;;
      l ) parameterL="$OPTARG" ;;
      j ) parameterJ="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$parameterI" ] || [ -z "$parameterO" ] || [ -z "$parameterL" ] || [ -z "$parameterJ" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

echo "input filename=$parameterI.fasta"
echo "output filename=$parameterO.xlsx"
echo "BLAST module path: $parameterL"
echo "BLAST nr database path: $parameterJ"
now=$(date +"%T")
echo "Current time : $now"
echo "-------------------------------------"
echo "MIP ORACLE"
echo "-------------------------------------"
# Begin script in case all parameters are correct
python MIP_1.py $parameterI
echo
echo
now=$(date +"%T")
echo "Current time : $now"
echo "__________________________________________"
echo "All possible MIPs have been generated according to the target region length and arm lengths provided in the config file."
python MIP_2.py $parameterI
echo
now=$(date +"%T")
echo "Current time : $now"
echo "__________________________________________"
echo "The MIPs have been filtered for GC content, Temperature, and PolyNs as per the config file."
python MIP_3.py
echo
now=$(date +"%T")
echo "Current time : $now"
echo "__________________________________________"
echo "BLAST input files have been generated, working on BLAST results now."
module load $parameterL
export BLASTDB="$parameterJ"
blastn -db nt -num_threads 48 -task blastn-short -query extension_arms.txt -taxids 9606 -max_target_seqs 10 -outfmt 5 -out Resultshuman_extarm.xml
blastn -db nt -num_threads 48 -task blastn-short -query extension_arms.txt -max_target_seqs 10 -outfmt 5 -out Resultsall_extarm.xml
echo
now=$(date +"%T")
echo "Current time : $now"
echo "__________________________________________"
echo "BLAST results have been generated against the human and non-human databases."
python MIP_4.py
python MIP_5.py
python MIP_6.py
echo
now=$(date +"%T")
echo "Current time : $now"
echo "__________________________________________"
echo "BLAST results against the general nt database have been parsed."
python MIP_7.py
python MIP_8.py
echo
now=$(date +"%T")
echo "Current time : $now"
echo "__________________________________________"
echo "BLAST results against the nt database filtering for humans have been parsed."
now=$(date +"%T")
echo "Current time : $now"
echo "__________________________________________"
echo "The MIPs have been filtered on the basis of BLAST matches found."
echo "The MIPs for which no human or matches for other organisms were present will be carried forward."
python MIP_9.py $parameterO
echo
now=$(date +"%T")
echo "Current time : $now"
echo "__________________________________________"
echo "The final results file has been generated."
echo
echo
echo "-------------------------------------"
echo "MIP ORACLE"
echo "-------------------------------------"
