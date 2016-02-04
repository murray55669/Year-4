% Secure Programming Lab 1: Data Corruption
% School of Informatics, University of Edinburgh
% 3pm-6pm, 2nd February 2016

Exercise 1
==========

## Part 1: classic stack overflow

**Checkpoint 1.** How can you tell the program will run as setuid root,
and how can you make a compiled program run as setuid root?

A) Listing the permission flags/ownership with "ls -all" shows the owner as root, and that anyone can execute the file with root's permissions ('s' flag for 'setuid' allows temporary privilege increase when executing the file)
To make the program run as setuid root, one needs to 'chmod' the permissions of the file. In this instance, 'cmod 6755 noticeboard' gives the specific permission set used. The file also needs to be owned by root for the setuid to do anything, so a 'chown root noticeboard'

**Checkpoint 2.** Briefly explain the output of these tools, and
how the compiler flags influence the output of `checksec.sh` (look
at the `Makefile` to see how `gcc` was invoked).
checksec.sh:
-no RELRO = the headers in the binary are never set to read only, meaning they can be modified during execution
-No canary found = there is no 'canary' protection on the stack, 'canary' bieng a value written to the stack that is to be checked before using the next piece of data (a function call return address, for instance) to ensure that the data has not been overwritten by a simple stack overflow - if the canary had been changed, it imples the memory on the stack has been tampered with
-NX disabled = 'non-executable' disabled, so there cannot be code that is segmented as purely data - anything in the program's memory region can be executed
-No PIE = 'position indipendent executable' - the memory layout of the program is static
-No RPATH/RUNPATH = there is no hard-coded location the application will check for libraries/executables it depends upon

rats:
'fixed size local buffer' - alerts that using a fixed-size buffer may result in stack overflows
'strcpy' - alerts that there is a risk of a buffer overflow if strcpy's argument are not limited


**Checkpoint 3.** Explain what your shellcode does and how you
  made it.
  
**Checkpoint 4.** Explain how your exploit works.

**Checkpoint 5.** Provide your patch to fix the notice board program
(use `diff -c <oldprogram> <newprogram>`).

## Part 2: another vulnerability

**Checkpoint 1.** Identify the security flaw in the new version of
  `noticeboard.c`; explain what it allows and demonstrate an exploit
  that compromises the standard system security.

**Checkpoint 2 (optional).** Briefly, explain how your root shell
 exploit works.

**Checkpoint 3.** Give a patch which fixes the second version of
  `noticeboard.c`.

Exercise 2
==========

**Checkpoint 1.** Explain the format of the messages sent by the client.

**Checkpoint 2.** Provide a program (or shell script) which crashes
  the server remotely.

**Checkpoint 3.** Give a patch to fix the problem(s).

Exercise 3 (Advanced)
=====================

**Checkpoint 1.**  How do you get the address of a `/bin/sh` string, and if you can't find one in memory how to inject one?

**Checkpoint 2.**  Where does the `system` function exist in libc?  Where is it loaded in your program?

**Checkpoint 3.**  How do you call `system` as you return from the overflown function with your string as its argument?

**Checkpoint 4.**  A program which crashes may leave a log file somewhere.  You should also ensure your program exits cleanly.  How do you do this?


Exercise 4 (Optional)
=====================

**Checkpoint 1.** Identify the security flaw in the code, and provide
  the relevant CVE number.

**Checkpoint 2.** Briefly summarise the problem and explain and why
  it is a security flaw.

**Checkpoint 3.** Give a recommendation for a way to repair the problem.

**Checkpoint 4 (very optional).** Build a *proof-of-concept* to
  demonstrate the security flaw and explain how it might be exploited;
  check that your repair (or the current released version) prevents
  your attack.

