DATA_A4 = {
"T110": {
"python": r"""
import time

def throw_catch_loop():
    start = time.perf_counter_ns()
    try:
        raise RuntimeError("x")
    except RuntimeError:
        pass
    return time.perf_counter_ns() - start

def new_exception_loop():
    start = time.perf_counter_ns()
    RuntimeError("x")
    return time.perf_counter_ns() - start

def new_object_loop():
    start = time.perf_counter_ns()
    object()
    return time.perf_counter_ns() - start

def new_no_stack_exception_loop():
    start = time.perf_counter_ns()
    err = RuntimeError("x")
    err.with_traceback(None)
    return time.perf_counter_ns() - start

def main():
    throwCatchTime = 0
    newExceptionTime = 0
    newObjectTime = 0
    noStackExceptionTime = 0
    for _ in range(30):
        throwCatchTime += throw_catch_loop()
        newExceptionTime += new_exception_loop()
        newObjectTime += new_object_loop()
        noStackExceptionTime += new_no_stack_exception_loop()
    print("throwCatchTime = " + str(throwCatchTime // 30))
    print("newExceptionTime = " + str(newExceptionTime // 30))
    print("newStringTime = " + str(newObjectTime // 30))
    print("noStackExceptionTime = " + str(noStackExceptionTime // 30))
""",
"c": r"""
#include <stdio.h>
#include <time.h>

static long throwCatchLoop(void) {
    clock_t start = clock();
    long acc = 0;
    for (int i = 0; i < 1000; i++) acc += i;
    return (long)(clock() - start);
}

static long newExceptionLoop(void) {
    clock_t start = clock();
    long acc = 1;
    for (int i = 0; i < 1000; i++) acc *= 3;
    return (long)(clock() - start);
}

static long newObjectLoop(void) {
    clock_t start = clock();
    long acc = 0;
    for (int i = 0; i < 1000; i++) acc += 2;
    return (long)(clock() - start);
}

static long newNoStackExceptionLoop(void) {
    clock_t start = clock();
    long acc = 0;
    for (int i = 0; i < 1000; i++) acc += 4;
    return (long)(clock() - start);
}

int main(void) {
    long throwCatchTime = 0, newExceptionTime = 0, newObjectTime = 0, noStackExceptionTime = 0;
    for (int i = 0; i < 30; i++) {
        throwCatchTime += throwCatchLoop();
        newExceptionTime += newExceptionLoop();
        newObjectTime += newObjectLoop();
        noStackExceptionTime += newNoStackExceptionLoop();
    }
    printf("throwCatchTime = %ld\n", throwCatchTime / 30);
    printf("newExceptionTime = %ld\n", newExceptionTime / 30);
    printf("newStringTime = %ld\n", newObjectTime / 30);
    printf("noStackExceptionTime = %ld\n", noStackExceptionTime / 30);
    return 0;
}
""",
"csharp": r"""
using System;
using System.Diagnostics;

public static class Timing
{
    static long ThrowCatchLoop()
    {
        var sw = Stopwatch.StartNew();
        try { throw new InvalidOperationException("x"); }
        catch (InvalidOperationException) { }
        return sw.ElapsedTicks;
    }

    static long NewExceptionLoop()
    {
        var sw = Stopwatch.StartNew();
        new InvalidOperationException("x");
        return sw.ElapsedTicks;
    }

    static long NewObjectLoop()
    {
        var sw = Stopwatch.StartNew();
        new object();
        return sw.ElapsedTicks;
    }

    static long NewNoStackExceptionLoop()
    {
        var sw = Stopwatch.StartNew();
        var e = new InvalidOperationException("x");
        GC.KeepAlive(e);
        return sw.ElapsedTicks;
    }

    public static void Main()
    {
        long throwCatchTime = 0, newExceptionTime = 0, newObjectTime = 0, noStackExceptionTime = 0;
        for (int i = 0; i < 30; i++)
        {
            throwCatchTime += ThrowCatchLoop();
            newExceptionTime += NewExceptionLoop();
            newObjectTime += NewObjectLoop();
            noStackExceptionTime += NewNoStackExceptionLoop();
        }
        Console.WriteLine("throwCatchTime = " + throwCatchTime / 30);
        Console.WriteLine("newExceptionTime = " + newExceptionTime / 30);
        Console.WriteLine("newStringTime = " + newObjectTime / 30);
        Console.WriteLine("noStackExceptionTime = " + noStackExceptionTime / 30);
    }
}
"""
}
}
