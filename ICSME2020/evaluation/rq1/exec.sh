#!/bin/bash

base=./outputs/normal/$1
echo $base
mkdir -p $base

  SECONDS=0
  file=$base/out.1.txt


  adb shell settings put global transition_animation_scale 0
  adb shell settings put global window_animation_scale 0
  adb shell settings put global animator_duration_scale 0

  echo -n "Running tests now."

  adb shell am instrument -w -r    -e class io.github.marktony.espresso.packages.AppNavigationTest#clickOnNavigationDrawerItem_ChangeTheme -e debug false io.github.marktony.espresso.test/android.support.test.runner.AndroidJUnitRunner >> $file
  
  echo "."
  echo "Finished."

  echo $SECONDS >> $base/time.txt

if [ $PID ]
then
  echo "kill stress"
  kill -9  $PID
fi
