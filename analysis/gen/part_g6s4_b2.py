DATA_B2 = {
"T229": {
"python": r"""
import threading

N = 5

lock = threading.Condition()

def run(id, token_holder):
    try:
        with lock:
            for i in range(5):
                while token_holder["token"] % N != id:
                    lock.wait()
                print(str(id) + " " + str(i))
                token_holder["token"] += 1
                lock.notify_all()
    except KeyboardInterrupt as e:
        import traceback
        traceback.print_exc()
""",
"c": r"""
#include <pthread.h>
#include <stdio.h>

#define N 5

static pthread_mutex_t lock_m = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t lock_c = PTHREAD_COND_INITIALIZER;
static int token = 0;

void run(int id) {
    pthread_mutex_lock(&lock_m);
    for (int i = 0; i < 5; i++) {
        while (token % N != id) pthread_cond_wait(&lock_c, &lock_m);
        printf("%d %d\n", id, i);
        token++;
        pthread_cond_broadcast(&lock_c);
    }
    pthread_mutex_unlock(&lock_m);
}
""",
"csharp": r"""
using System;
using System.Threading;

public class Printer
{
    private const int N = 5;
    private static readonly object lockObj = new object();
    private static int token = 0;

    public void Run(int id)
    {
        try
        {
            lock (lockObj)
            {
                for (int i = 0; i < 5; i++)
                {
                    while (token % N != id) Monitor.Wait(lockObj);
                    Console.WriteLine(id + " " + i);
                    token++;
                    Monitor.PulseAll(lockObj);
                }
            }
        }
        catch (ThreadInterruptedException e)
        {
            Console.Error.WriteLine(e.StackTrace);
        }
    }
}
"""
}
}
