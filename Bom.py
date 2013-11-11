# -*- coding: utf-8 -*-


class Bom():
    BOM = {}

    def __init__(self, ):
        self.BOM.clear()

    def cargar_bom(self, listado):
        """
        Carga el BOM a partir de una lista de tuplas
        del tipo (codigo, cantidad, tiempo_fabricacion)
        """

        for tupla in listado:
            codigo = tupla[0]
            cantidad = tupla[1]
            tiempo = tupla[2]

            if codigo not in self.BOM:
                self.BOM[codigo] = [int(cantidad), float(tiempo)]
            else:
                #import ipdb; ipdb.set_trace()
                self.BOM[codigo][0] = self.BOM[codigo][0] + int(cantidad)

    def obtener_bom(self):
        return self.BOM
