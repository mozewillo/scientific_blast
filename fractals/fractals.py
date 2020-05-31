import argparse
import numpy as np
import matplotlib.pyplot as plt


parser=argparse.ArgumentParser(description='Specify the parameters to create beautiful fractal.')
parser.add_argument('-mx','--x_min', type=float, required=True, help="minimum value x")
parser.add_argument('-Mx','--x_max', type=float, required=True, help="maximum value x")
parser.add_argument('-lx','--lx', type=float, required=True, help="number of x poins")
parser.add_argument('-my','--y_min', type=float, required=True, help="maximum value y")
parser.add_argument('-My','--y_max', type=float, required=True, help="maximum value y")
parser.add_argument('-ly','--ly', type=float, required=True, help="number of y points")
parser.add_argument('-f','--f', type=str, required=True, help="choose set (mandelbrot / julia)")
parser.add_argument('-s','--s', type=str, required=False, help="save format (pdf / png)", default=None)
parser.add_argument('-n', '--n', type=str, required=False, help="file name to save", default="fractal")
parser.add_argument('-t' , '--t', type=str, required=False, help="title", default=None)
parser.add_argument('-ca', '--ca', type=float, required=False, help="the real part, if you are choosing Julia set", default=-0.75)
parser.add_argument('-cb', '--cb', type=float, required=False, help="the imaginary part, if you are choosing Julia set", default=-0.2)
parser.add_argument('-col', '--color', type=str, required=False, help="color", default="inferno")
parser.add_argument('-mi','--max_iter', type=float, required=False, help="maximal iteration", default=1000)
parser.add_argument('-mv','--max_val', type=float, required=False, help="maximal value", default=2)

args = parser.parse_args()


def julia_value(z, n):
    if n == 0:
        juli = z
    else:
        juli = julia_value(z, n-1)**2+c
    return juli

def mandelbrot_value(z, n):
    if n == 0:
        mandel = 0
    else:
        mandel = mandelbrot_value(z, n-1)**2+z
    return mandel

# more complex :)

def julia(z, n, max_val):
    c = complex(args.ca, args.cb)
    juli = z
    for x in range(n):
        juli = juli**2 + c
        if abs(juli) > max_val:
            return x
    return n

def mandelbrot(z, n, max_val):
    mandel = 0
    for x in range(n):
        mandel = mandel**2+z
        if abs(mandel) > max_val:
            return x
    return n


def approx(xrang, yrang, max_iter, max_val, f):
    for x in range(len(xrang) - 1):
        for y in range(len(yrang) -1):
        	A[x][y] = (f(B[x][y], max_iter, max_val))
    return A

def approx_from_val(xrang, yrange, max_iter, max_val, f):
    for x in range(len(xrang)):
        for y in range(len(yrange)):
            if B[x][y] < max_val:
                for i in range(max_iter):
                    if abs(f(B[x][y], i)) > max_val:
                        A[x][y] = i
                        break
            else:
                A[x][y]=0
    return A
    

if __name__ == '__main__':

    xrang = np.linspace(args.x_min, args.x_max, int(args.lx))
    yrange = np.linspace(args.y_min, args.y_max, int(args.ly))

    A = np.zeros((len(xrang), len(yrange))) #matrix to modify
    B = xrang+ yrange[:,None]*1j #matrix from vectors
    B = B.transpose()

    if args.f == "julia":
        A = approx(xrang, yrange, args.max_iter, args.max_val, f=julia)
    elif args.f == "mandelbrot":
        A = approx(xrang, yrange, args.max_iter, args.max_val, f=mandelbrot)
    elif args.f == "julia_value":
        A = approx_form_val(xrang, yrange, args.max_iter, args.max_val, f=julia_value)
    elif arg.f == "mandelbrot_value":
        A = approx_form_val(xrang, yrange, args.max_iter, args.max_val, f=mandelbrot_value)
    else:
        print ("Invalid function argument")

# show results
    if args.s == "txt":
        np.save("set_matrix.npy", A)
        
    if args.t:
        title = args.t
    else: title = args.f

    plt.title(title)
    plt.imshow(A, cmap=args.color)

# save to file
    if args.s == "png":
        name = args.n + '.png'
        plt.savefig(name)
    if args.s == "pdf":
        name = args.n + '.pdf'
        plt.savefig(name)
 
    plt.show()
