#include <sys/types.h>
#include <fcntl.h>
#include <stdio.h>


int main()
{
    int fd;
    const char buf[2] = "AA";
    fd = open("/dev/alina-dev",O_RDWR);
    if (fd < 0)
    {
        printf("Cannot open, use 'sudo'\n");
        return 0;
    }
    write(fd, buf, 2);
    printf("In your buffer: %s\n", buf);

    close(fd);
    return 0;
}
