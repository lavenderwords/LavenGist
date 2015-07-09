function GetPID #User #Name
{
PsUser=$1
PsName=$2
pid=$(ps -u $PsUser|grep $PsName|grep -v grep|grep -v vi|grep -v dbx|grep -v tail|grep -v start|grep -v stop |sed -n 1p |awk '{print $1}')
echo $pid
}

function GetCpu
{
CpuValue=$(ps -p $1 -o pcpu |grep -v CPU | awk '{print $1}' | awk -F. '{print $1}')
echo $CpuValue
}

username=${1}
processname=${2}
interval=${3}
count=${4}

for((i=1;i<$count;i++));do
pid=$(GetPID $username $processname)
usage=$(GetCpu $pid)
echo ZZZZ,$(date)>>$username$processname.log
echo $usage>>$username$processname.log
sleep $interval
done


