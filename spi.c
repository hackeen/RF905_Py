#include <Python.h>
#include <stdint.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/types.h>
#include <linux/spi/spidev.h>

static int fd = -1; // Initialize to an invalid file descriptor

static void pabort(const char *s) {
    perror(s);
    abort();
}

static const char *device = "/dev/spidev0.0";
static uint8_t mode;
static uint8_t bits = 8;
static uint32_t speed = 500000;
static uint16_t delay;

// Function to open the SPI port
static PyObject* openSPI(PyObject *self, PyObject *args, PyObject *kwargs) {
    static char* kwlist[] = {"device", "mode", "bits", "speed", "delay", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|siiii:openSPI", kwlist, &device, &mode, &bits, &speed, &delay))
        return NULL;

    fd = open(device, O_RDWR);
    if (fd < 0)
        pabort("can't open device");

    ret = ioctl(fd, SPI_IOC_WR_MODE, &mode);
    if (ret == -1)
        pabort("can't set SPI mode");

    ret = ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
    if (ret == -1)
        pabort("can't set bits per word");

    ret = ioctl(fd, SPI_IOC_WR_MAX_SPEED_HZ, &speed);
    if (ret == -1)
        pabort("can't set max speed hz");

    PyObject* retDict = PyDict_New();
    PyDict_SetItem(retDict, PyString_FromString("mode"), PyInt_FromLong((long)mode));
    PyDict_SetItem(retDict, PyString_FromString("bits"), PyInt_FromLong((long)bits));
    PyDict_SetItem(retDict, PyString_FromString("speed"), PyInt_FromLong((long)speed));
    PyDict_SetItem(retDict, PyString_FromString("delay"), PyInt_FromLong((long)delay));

    return retDict;
}

// Function to transfer data over SPI
static PyObject* transfer(PyObject* self, PyObject* arg) {
    PyObject* transferTuple;

    if (!PyArg_ParseTuple(arg, "O", &transferTuple))
        return NULL;

    if (!PyTuple_Check(transferTuple))
        pabort("Only accepts a single tuple as an argument\n");

    uint32_t tupleSize = PyTuple_Size(transferTuple);

    uint8_t tx[tupleSize];
    uint8_t rx[tupleSize];
    PyObject* tempItem;

    uint8_t i = 0;

    while (i < tupleSize) {
        tempItem = PyTuple_GetItem(transferTuple, i);
        if (!PyInt_Check(tempItem)) {
            pabort("non-integer contained in tuple\n");
        }
        tx[i] = (uint8_t)PyInt_AsSsize_t(tempItem);
        i++;
    }

    struct spi_ioc_transfer tr = {
        .tx_buf = (unsigned long)tx,
        .rx_buf = (unsigned long)rx,
        .len = tupleSize,
        .delay_usecs = delay,
        .speed_hz = speed,
        .bits_per_word = bits,
        .cs_change = 1,
    };

    ret = ioctl(fd, SPI_IOC_MESSAGE(1), &tr);
    if (ret < 1)
        pabort("can't send SPI message");

    PyObject* transferResult = PyTuple_New(tupleSize);
    for (i = 0; i < tupleSize; i++)
        PyTuple_SetItem(transferResult, i, Py_BuildValue("i", rx[i]));

    return transferResult;
}

// Function to close the SPI port
static PyObject* closeSPI(PyObject* self, PyObject* args) {
    if (fd != -1) {
        close(fd);
        fd = -1; // Set to an invalid value after closing
    }
    Py_RETURN_NONE;
}

static PyMethodDef SpiMethods[] = {
    {"openSPI", openSPI, METH_KEYWORDS, "Open SPI Port."},
    {"transfer", transfer, METH_VARARGS, "Transfer data."},
    {"closeSPI", closeSPI, METH_NOARGS, "Close SPI port."},
    {NULL, NULL, 0, NULL}
};

// Module initialization function
PyMODINIT_FUNC initspi(void) {
    (void) Py_InitModule("spi", SpiMethods);
}
