
#!/bin/bash
echo "Please only use simple math problems (+-/*) and enter it here: "
read math_problem
echo "Here is your result: $math_problem"
<<<<<<< HEAD
=======
read -r var1 var2 var3 <<< "$math_problem"

case $var2 in
	+)
	math_add=$((var1 + var3))
	echo "Result is: $math_add"
	;;

	-)
	math_sub=$((var1 - var3))
	echo "Result is: $math_sub"
	;;

	/)
	math_div=$((var1 / var3))
	echo "Result is: $math_div"
	;;

	*)
	math_mult=$((var1 * var3))
	echo "Result is: $math_mult"
	;;

esac

>>>>>>> cde72c333e59a05a2558070aaf950ac0a4d9cc4d
