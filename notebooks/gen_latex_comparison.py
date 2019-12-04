import os

if __name__ == '__main__':
    with open("comparison.tex", 'w') as f:
        f.write("\\documentclass[english]{article}\n")
        f.write("\\usepackage{graphicx}\n")
        f.write("\\usepackage{caption}\n")
        f.write("\\usepackage{subcaption}\n")
        f.write("\\begin{document}\n")
        f.write("\\title{Comparison of fits}\n")

        linear_files = os.listdir("linear_fit")
        logari_files = os.listdir("logarithmic_fit")

        linear_files.sort()
        logari_files.sort()

        figs_per_page = 3
        figs_counter = 0

        for (lin, log) in zip(linear_files, logari_files):
            f.write("""
            \\begin{figure}
            \\centering
            \\begin{subfigure}{.5\\textwidth}
            \\centering
            \\includegraphics[width=\\linewidth]{""" +
                    "linear_fit/" + lin +
                    """}
                    \\caption{Linear Least Squares Fit}
            \\end{subfigure}%
            \\begin{subfigure}{.5\\textwidth}
            \\centering
                    \\includegraphics[width=\\linewidth]{""" +
                    "logarithmic_fit/" + log +
                    """}
            \\caption{Logarithmic Least Squares Fit}
            \\end{subfigure}
            \\end{figure}
            """)

            figs_counter += 1
            if figs_counter == figs_per_page:
                f.write("\\clearpage\n")
                figs_counter = 0

        f.write("\\end{document}\n")
