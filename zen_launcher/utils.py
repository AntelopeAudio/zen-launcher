def vercmp(v1, v2):
    def norm(v):
        return list(map(int, v.split('.')))
    nv1 = norm(v1)
    nv2 = norm(v2)
    return (nv1 > nv2) - (nv1 < nv2)
