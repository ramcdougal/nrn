#!/bin/sh

a=$1
if test "$a" = "" ; then
	a=.
fi
cd $a

if hg identify > /dev/null && test -d .hg ; then
	gcs=`hg identify -i`
	lcs=`hg identify -n`
	branch="`hg identify -b`"
	tags="`hg identify -t`"
	sha=`echo $gcs | sed 's/\+//'`
	d=`hg log -r $sha --template '{date|shortdate}'`
	echo "#define HG_DATE \"$d\""
	echo "#define HG_BRANCH \"$branch\""
	echo "#define HG_CHANGESET \"$gcs\""
	echo "#define HG_LOCAL \"$lcs\""
	echo "#define HG_TAG \"$tags\""
elif test -f src/nrnoc/nrnversion.h ; then
	sed -n '1,$p' src/nrnoc/nrnversion.h
else
	echo "#define HG_DATE \"1999-12-31\""
	echo "#define HG_BRANCH \"\""
	echo "#define HG_CHANGESET \"?\""
	echo "#define HG_LOCAL \"?\""
	echo "#define HG_TAG \"\""
	exit 1
fi

