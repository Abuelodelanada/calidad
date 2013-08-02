# -*- coding: utf-8 -*-


class Mrp():

    def __init__(self, ):
        """
        """

    def calucar_necesidades(self, bom, inventario, cantidad):
        """
        Calula las necesidades de MP a partir de:
        - Bom del producto
        - Inventario de MP y SE
        - Cantidad del producto a fabricar
        """
        bom = bom.obtener_bom()
        inventario = inventario.obtener_inventario()
        totales = {}
        self.necesidades = {}

        for i in bom:
            totales[i] = cantidad * bom[i]

        for t in totales:
            if t in inventario:
                if inventario[t] <= totales[t]:
                    self.necesidades[t] = totales[t] - inventario[t]
            else:
                self.necesidades[t] = totales[t]

    def obtener_necesidades(self):
        return self.necesidades


        print totales
        print inventario
        print necesidades
        print cantidad
