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


def figure3d(gates, directory):
    assert len(set([gate.cargo for gate in gates])) == 1
    matrix_file = f"{directory}/similarity_matrix_{gates[0].cargo}.dat"
    scores = similarity_table([g.log().normal() for g in gates])
    scores = scores.rename(gate_drop_name, axis='index')
    scores = scores.rename(gate_drop_name, axis='columns')

    with open(matrix_file, 'w') as f:
        f.write(scores.to_csv())

    return scores


def figure3bc(gates, directory, name):
    matrix_file = f"{directory}/compat_matrix_{name}.dat"
    scores = reduced_compatibility_table(gates)

    with open(matrix_file, 'w') as f:
        f.write(scores.to_csv())

    return scores


def figure5(data, A, B, directory):
    def remove_negative(numpy_array):
        filtered = [row for row in numpy_array if row[0] > 0.0 and row[1] > 0.0]
        return numpy.vstack(tuple(filtered))

    for ref in data[A.strain:A.backbone:]:
        unknown = data[B.strain:B.backbone:ref.cargo]
        if unknown:
            guess_points, solution = linear_transform_prediction(A, B, ref)
            guess_points = remove_negative(guess_points)
            guess = Gate(f"{unknown.name}",
                         [],
                         guess_points[:, 0],
                         guess_points[:, 1])

            scatter, curve = guess.to_gnuplot(directory)


def figureS1(data, directory):
    for strain in data.strains:
        matrix_file = f"{directory}/compat_matrix_{strain}_Strain.dat"
        scores = reduced_compatibility_table(data[strain::])

        with open(matrix_file, 'w') as f:
            f.write(scores.to_csv())

    return scores


def figureS3(data, directory):
    for cargo in data.plasmids[3:]:
        gates = data[::cargo]
        assert len(set([gate.cargo for gate in gates])) == 1
        matrix_file = f"{directory}/similarity_matrix_{cargo}.dat"
        scores = similarity_table([g.log().normal() for g in gates])
        scores = scores.rename(gate_drop_name, axis='index')
        scores = scores.rename(gate_drop_name, axis='columns')

        with open(matrix_file, 'w') as f:
            f.write(scores.to_csv())


def figureS4(data, directory):
    contexts = data.contexts
    for strain, backbone in contexts:
        matrix_file = f"{directory}/score_matrix_{strain}_{backbone}.dat"
        gates = data[strain:backbone:]
        scores = score_table(gates)
        scores = scores.rename(gate_drop_context, axis='index')
        scores = scores.rename(gate_drop_context, axis='columns')

        with open(matrix_file, 'w') as f:
            f.write(scores.to_csv())

    return scores
