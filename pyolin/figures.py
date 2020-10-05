<<<<<<< HEAD
from pyolin import FIGDIR
from pyolin import RESDIR
import numpy
from pyolin.analysis import similarity_table


def figure2(gateA_list, gateB_list):
    case = f"figure2_with_{gateA_list[0].cargo}_vs_{gateB_list[0].cargo}"
    with open(f"{FIGDIR / 'Figure2'}/{case}.gnuplot", 'w') as f:

        print(f"load '{FIGDIR / 'Figure2/style.gnuplot'}'", file=f)
        print(f"set output '{FIGDIR / 'Figure2'}/{case}.eps'", file=f)

        for a, b in zip(gateA_list, gateB_list):
            assert a.backbone == b.backbone and a.strain == b.strain

            a_scatter, a_curve = a.to_gnuplot(RESDIR)
            b_scatter, b_curve = b.to_gnuplot(RESDIR)
            print(f"set title '{a.strain} {a.backbone}' font ',32", file=f)
            print("plot \\", file=f)
            print(f"'{a_scatter}' u 2:3 ls 1 notitle, \\", file=f)
            print(f"'{a_curve}' u 1:2 w l ls 2 notitle, \\", file=f)

            print(f"'{b_scatter}' u 2:3 ls 3 notitle, \\", file=f)
            print(f"'{b_curve}' u 1:2 w l ls 4 notitle", file=f)
=======
import numpy
from pyolin.gate import Gate
from pyolin.linear_transform import linear_transform_prediction
from pyolin.analysis import similarity_table
from pyolin.analysis import reduced_compatibility_table
from pyolin.analysis import score_table


def figure2(gateA_list, gateB_list, directory):
    for a, b in zip(gateA_list, gateB_list):
        assert a.backbone == b.backbone and a.strain == b.strain

        a_scatter, a_curve = a.to_gnuplot(directory)
        b_scatter, b_curve = b.to_gnuplot(directory)
>>>>>>> d24d2f9d92c89a0a1041c93f2c273a166c89e461


def gate_drop_name(gate_namestring):
    strain = gate_namestring.split('_')[0]
    backbone = gate_namestring.split('_')[1]
    return f"\\\\shortstack{{{strain}\\\\\\\\ {backbone}}}"


def gate_rename(gate_namestring):
    splut = gate_namestring.split('_')
    strain = splut[0]
    backbone = splut[1]
    cargo = splut[-2] + ' ' + splut[-1].upper()
    return f"{cargo} in {strain} with {backbone}"


def gate_drop_context(gate_namestring):
    splut = gate_namestring.split('_')
    return f"{splut[-2]} {splut[-1].upper()}"


def similaritymap(gates, directory):
    if len(set([gate.cargo for gate in gates])) != 1:
        return
    casename = f"similarity_matrix_{gates[0].cargo}"
    matrix_file = f"{RESDIR / casename}.dat"
    scores = similarity_table([g.log().normal() for g in gates])
    scores = scores.rename(gate_drop_name, axis='index')
    scores = scores.rename(gate_drop_name, axis='columns')

    with open(matrix_file, 'w') as f:
        f.write(scores.to_csv())

    with open(f"{directory}/{casename}.gnuplot", 'w') as f:
        print(f"load '{directory}/style.gnuplot'", file=f)
        print(f"set output '{directory}/{casename}.eps'", file=f)
        print((f"set title 'Inter-context Similarity Scores for "
               f"{gates[0].cargo.split('_')[0]} "
               f"{gates[0].cargo.split('_')[1].upper()}' "
               f"font ',32'"),
              file=f)

        print("unset key", file=f)

        print("set datafile separator comma", file=f)
        print((f"plot '{matrix_file}' matrix rowheaders columnheaders "
               f"using 1:2:3 with image"),
              file=f)
    return scores


from pyolin.analysis import compatibility_table
from pyolin.analysis import reduced_compatibility_table


def compatmap(gates, name, directory):
    matrix_file = f"{RESDIR}/compat_matrix_{name}.dat"
    scores = reduced_compatibility_table(gates)

    with open(matrix_file, 'w') as f:
        f.write(scores.to_csv())

    with open(f"{directory}/compat_map_{name}.gnuplot", 'w') as f:
        print(f"load '{directory}/style.gnuplot'", file=f)
        print(f"set output '{directory}/{name}_compat_map.eps'", file=f)
        print((f"set title 'Compatibility Table for "
               f"{name.replace('_', ' ')}' "
               f"font ',30'"),
              file=f)

        print("unset key", file=f)

        print("set datafile separator comma", file=f)
        print((f"plot '{matrix_file}' matrix rowheaders columnheaders "
               f"using 1:2:3 with image"),
              file=f)
        print("set datafile separator", file=f)

    return scores


# def figure5(data, A, B, directory):
#     def remove_negative(numpy_array):
#         filtered = [row for row in numpy_array if row[0] > 0.0 and row[1] > 0.0]
#         return numpy.vstack(tuple(filtered))
    
#     for ref in data[A.strain:A.backbone:]:
#         unknown = data[B.strain:B.backbone:ref.cargo]
#         if unknown:
#             guess_points, solution = linear_transform_prediction(A, B, ref)
#             guess_points = remove_negative(guess_points)
#             guess = Gate(f"{ref.name}_guess",
#                          [],
#                          guess_points[:, 0],
#                          guess_points[:, 1])

#             scatter, curve = guess.to_gnuplot(directory)
#             guess_scatter = f"predict_{unknown.name}_from_{A.name}_and_{B.name}_scatter.csv"
#             guess_curve = f"predict_{unknown.name}_from_{A.name}_and_{B.name}_curve.csv"
#             scatter, curve = unknown.to_gnuplot(directory)
            
#             os.rename(scatter, guess_scatter)
#             os.rename(curve, guess_curve)
#             with open(f"{directory}/predict_{unknown.name}_from_{A.name}_and_{B.name}.gp", 'w') as f:

#                 print("reset session", file=f)
#                 print(figure2_style, file=f)

#                 print("set output 'predict_{unknown.name}_from_{A.name}_and_{B.name}.eps'", file=f)

#                 print((f"set title 'Prediction for "
#                        f"{name.replace('_', ' ')}' "
#                        f"font 'Computer Modern Roman,30'"),
#                       file=f)

#                 print("unset key", file=f)

#                 print("set datafile separator comma", file=f)
#                 print((f"plot '{matrix_file}' matrix rowheaders columnheaders "
#                        f"using 1:2:3 with image"),
#                       file=f)
#                 print("set datafile separator", file=f)
