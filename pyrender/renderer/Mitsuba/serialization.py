import struct
import zlib

def serialize_mesh(mesh, normals=None, colors=None, uvs=None):
    assert(mesh.dim == 3);
    assert(mesh.vertex_per_face == 3);

    name = b"Generated by PyMesh";
    header1 = int('041c', 16);
    header2 = int('0004', 16);
    header = struct.pack("<HH", header1, header2);
    data_flags = 1<<13; # Double precision.

    vertices = mesh.vertices;
    vertex_data = b''.join([struct.pack("<ddd", v[0], v[1], v[2])
        for v in mesh.vertices ]);
    face_data = b''.join([struct.pack('<III', f[0], f[1], f[2])
        for f in mesh.faces]);

    if normals is not None and len(normals) == mesh.num_vertices:
        data_flags |= 1;
        normal_data = b''.join([struct.pack('<ddd', n[0], n[1], n[2])
            for n in normals]);
    else:
        print("no normal");
        print(mesh.num_vertices)
        print(normals.shape);
        normal_data = b'';

    if colors is not None and len(colors) == mesh.num_vertices:
        data_flags |= 8;
        color_data = b''.join([struct.pack('<ddd', c[0], c[1], c[2])
            for c in colors]);
    else:
        color_data = b'';

    if uvs is not None and len(uvs) == mesh.num_vertices:
        data_flags |= 2;
        uv_data = b''.join([struct.pack('<dd', uv[0], uv[1])
            for uv in uvs])
    else:
        uv_data = b'';

    mesh_header = struct.pack("<I{}sQQ".format(len(name)+1), data_flags,
            name, mesh.num_faces * 3, mesh.num_faces);

    mesh_data = mesh_header + vertex_data + \
            normal_data + uv_data + color_data + face_data;
    mesh_data = zlib.compress(mesh_data);
    footer = struct.pack("<QI", 0, 1);

    data = header + mesh_data + footer;
    return data;
