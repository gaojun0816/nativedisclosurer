# Description
As for Android Apps, development can be done both with VM language (i.e., Java/Kotlin) and Native language (i.e., C/C++). The VM code will be compiled as *Bytecode* and stored as *DEX* files (i.e., \*.dex) in an APK file, while The native code will be compiled as *binary* code and stored as *shared library* files (i.e., \*.so). The invocation between the 2 languages is realized by using **JNI** APIs.

However, for most of Android app analysis tools, native part of Android apps is normally ignored. This could lead to blind-spot in certain analyses under situations such as:

> VMethod<sub>1</sub> --> NFuction --> VMethod<sub>2</sub> --> VMethod<sub>3</sub>

*VMethod* indicates methods in VM code while *NFunction* stands for functions in native code. In this case, the last 2 VM methods (i.e., *VMethod<sub>2</sub>* and *VMethod<sub>3</sub>*) could be missing by an analysis since they are "blocked" by the native function (i.e., *NFunction*).

**This Tool** is to cop with such an awkward situation by report the **Entry** methods (i.e., VMethod<sub>1</sub> in this case) and the **Exit** methods (i.e., VMethod<sub>2</sub> in this example).

# Requirement
+ Tested with Python 3.7.7.
+ `pip install -r requirements.txt`

## Known issues
+ Python 3.7.0 has a bug with *zipfile* which leads to failure of loading *shared library* files.
+ Python 3.9 will lead to *lock cannot be used* error.

# Usage
This tool takes **APK** files as input. You can use `Python main.py --help` to check the usage of the tool.

## Limitation
+ to analyze a certain JNI function (i.e., functions in native code which have counterpart methods in VM code) or *JNI_OnLoad* function for dynamic registration of JNI functions, the time limit is set to 180 600 seconds respectively. Thus, for large JNI functions, the result could be missing. To increase the analysis time limit, reset the `WAIT_TIME` and `DYNAMIC_ANALYSIS_TIME` value in `main.py`.
+ this tool is developed based on [Angr](https://angr.io/) framework. To avoid the analysis to go too deep into the path of a state, the [`LengthLimiter`](https://docs.angr.io/core-concepts/pathgroups) is set to 500 and 1000 repectively for analyzing JNI functions and *JNI_OnLoad*. This value can be adjusted by reset the `MAX_LENGTH` and `DYNAMIC_ANALYSIS_LENGTH` value in `jni_interfaces/utils.py`.

# Output
For app named *example-app.apk*, by default, a folder named *example-app_result* will be created. In this folder, for each *shared library* file in the APK which contains JNI functions invoked by VM code, a counterpart result file will be generated with suffix *\*.result*. The result files are CSV files with following fields:
+ invoker_cls: class of **Entry** method
+ invoker_method: name of **Entry** method
+ invoker_signature: signature of **Entry** method
+ invoker_symbol: the corresponding symbol's name of the **Entry** method in the *shared library*. This name could be the name of the counterpart JNI function or a random name generated by the compiler or even *None* if it is stripped by the compiler.
+ invoker_static_export: boolean value to indicate whether the counterpart JNI function of the **Entry** method is statically exported by using **JNIEXPORT** or dynamically exported by using **RegisterNatives** JNI API function.
+ invokee_cls: class of **Exit** method
+ invokee_method: name of **Exit** method
+ invokee_signature: signature of **Exit** method
+ invokee_static: boolean value indicates whether the **Exit** method is a static method
+ invokee_desc: if there are failures in parsing certain parts of **Exit** method, there may be some reason given here

There will be a *performance* file generated which states the performance of the tool when analyzing the APK. This file contains following fields:
+ elapsed: the time used to analyze the APK in seconds.
+ analyzed_so: number of analyzed *shared library* files. This number should equal to the number of *\*.so* files contained in the APK but more than the *\*.result* files in the result folder. Since there could be *\*.so* files contained in the APK but not really used.
+ analyzed_func: number of C JNI functions analyzed. This number should equal to the C JNI functions that have counterpart Java native methods.
+ func_timeout: number of C JNI functions that are timeout when analyzing. As there is a time limitation for analyzing each C JNI function.
+ dynamic_timeout: this is a count indicates how many analyses of dynamic JNI function registration is timeout. Since when such an analysis timeout, the dynamically registered C JNI functions will highly possibly not be detected.
