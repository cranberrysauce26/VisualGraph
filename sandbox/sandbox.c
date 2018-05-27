#include <stdio.h>
#include <seccomp.h>    // MAIN LIBRARY!!!
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/prctl.h>
#include <sys/socket.h>   // for AF_UNIX
#include <sys/resource.h> // for resource limits

#include <stdlib.h> // not needed

int load_seccomp() {
    prctl(PR_SET_NO_NEW_PRIVS, 1);
    // TODO: research the syscalls below more thoroughly
    int syscalls_whitelist[] = 
                            {
                                /**** standard ***/
                                SCMP_SYS(read), SCMP_SYS(fstat),
                                SCMP_SYS(lstat), SCMP_SYS(getcwd),
                                SCMP_SYS(mmap), SCMP_SYS(mprotect),
                                SCMP_SYS(munmap), SCMP_SYS(uname),
                                SCMP_SYS(arch_prctl), SCMP_SYS(brk),
                                SCMP_SYS(access), SCMP_SYS(exit_group),
                                SCMP_SYS(close), SCMP_SYS(readlink),
                                SCMP_SYS(sysinfo), SCMP_SYS(write),
                                SCMP_SYS(writev), SCMP_SYS(lseek),
                                SCMP_SYS(stat), 
                                /**** maybe a bit sketchy? ****/
                                SCMP_SYS(rt_sigaction),
                                SCMP_SYS(rt_sigprocmask), SCMP_SYS(prlimit64), 
                                SCMP_SYS(set_tid_address), SCMP_SYS(getrandom),
                                SCMP_SYS(sigaltstack), SCMP_SYS(getdents),
                                SCMP_SYS(fcntl), SCMP_SYS(getpid),
                                SCMP_SYS(ioctl), SCMP_SYS(dup), /* I think dup might be unsafe */
                                SCMP_SYS(geteuid), SCMP_SYS(getuid),
                                SCMP_SYS(getegid), SCMP_SYS(getgid),
                                SCMP_SYS(set_robust_list), SCMP_SYS(futex),
                                SCMP_SYS(execve),
                                /*** Required network syscalls by Python3 ***/
                                SCMP_SYS(connect), /*SCMP_SYS(socket),*/
                                /*** Required by node ***/
                                SCMP_SYS(clock_getres), SCMP_SYS(epoll_create1),
                                SCMP_SYS(pipe2), SCMP_SYS(eventfd2), SCMP_SYS(clone),
                                SCMP_SYS(madvise), SCMP_SYS(epoll_ctl),
                                SCMP_SYS(epoll_wait), SCMP_SYS(exit), SCMP_SYS(poll)
                            };

    int syscalls_whitelist_length = sizeof(syscalls_whitelist) / sizeof(int);
    scmp_filter_ctx ctx = NULL;
    // load seccomp rules
    ctx = seccomp_init(SCMP_ACT_KILL);
    if (ctx == NULL) {
        return 1;
    }
    for (int i = 0; i < syscalls_whitelist_length; ++i) {
        if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, syscalls_whitelist[i], 0) != 0) {
            return 1;
        }
    }
    /************ Special seccomp rules *****************/
    // do not allow "w" and "rw" and "a"
    if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 1, SCMP_CMP(1, SCMP_CMP_MASKED_EQ, O_WRONLY | O_RDWR | O_APPEND, 0)) != 0) {
        return 1;
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat), 1, SCMP_CMP(2, SCMP_CMP_MASKED_EQ, O_WRONLY | O_RDWR | O_APPEND, 0)) != 0) {
        return 1;
    }

    /* allow local socket for python using AF_UNIX. But no other sockets!! */
    if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(socket), 1, SCMP_CMP(0, SCMP_CMP_EQ, AF_UNIX)) != 0) {
        return 1;
    }

    if (seccomp_load(ctx) != 0) {
        return 1;
    }
    seccomp_release(ctx);
    return 0;
}

int load_rlimits() {
    struct rlimit r;
    r.rlim_cur = 2; // 2 second cpu limit
    if (setrlimit(RLIMIT_CPU, &r) != 0) return 1;
    return 0;
}

/**
 * The main function's argument rules (for now).
 * argv[1] is stdin
 * argv[2] is stdout and stderr
 * argv[3] is the ABSOLUTE path to the executable (this can be changed to search in PATH environment var)
 * argv[4...arc-1] are the arguments passed to the executable
 */
int main(int argc, char *argv[]) {
    int input_fildes = open(argv[1], O_RDONLY);
    int output_fildes = open(argv[2], O_WRONLY);

    // redirect stdin to input_fildes
    dup2(input_fildes, STDIN_FILENO);

    // redirect stdout to output_fildes
    dup2(output_fildes, STDOUT_FILENO);

    // redirect stderr to output_fildes
    dup2(output_fildes, STDERR_FILENO);

    char **program_args = argv+3;

    for (int i = 0; ; ++i) {
        if (program_args[i]==NULL) {
            break;
        } else {
            printf("args[%d] = %s\n", i, program_args[i]);
        }
    }

    if (load_seccomp() != 0) {
        return 1;
    }
    if (load_rlimits() != 0) {
        return 1;
    }

    execv(program_args[0], program_args);

    // while (1){}

    // int fd = open("input.txt", O_RDONLY);
 
    // printf("opened fd\n");

    // FILE* read_fp = fopen("input.txt", "r");
    // printf("read open file\n");
    // int read_int;
    // fscanf(read_fp, "%d", &read_int);
    // printf("read_int = %d\n", read_int);
    // printf("finished reading\n");
    // fclose(read_fp);

    // char *args[] = {"/usr/bin/python3", "tests/test4.py", NULL};
    // // char *args[] = {"/usr/bin/node", "hey.js", NULL};
    // // char *args[] = {"./test", NULL};
    // // char *args[] = {"/usr/bin/ping", "google.com", NULL};
    // char *env[] = {NULL};
    // printf("executing\n");
    // execve(args[0], args, env);
    // printf("finished executing\n");
    // // return 0;

    // FILE* write_fp = fopen("output.txt", "a+");
    // printf("write open file\n");
    // fprintf(write_fp, "this is me\n");
    // printf("fnished writing\n");
    // fclose(write_fp);
}