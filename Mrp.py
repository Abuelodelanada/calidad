# -*- coding: utf-8 -*-


class Mrp():

    necesidades = {}

    def __init__(self, ):
        """
        """
        self.necesidades.clear()

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

        for i in bom:
            totales[i] = cantidad * bom[i][0]

        for t in totales:
            if t in inventario:
                if inventario[t] <= totales[t]:
                    resta = totales[t] - inventario[t]
                    tiempo = resta * bom[t][1]
                    self.necesidades[t] = [resta, tiempo]
            else:
                tiempo = resta * bom[t][1]
                self.necesidades[t] = [totales[t], tiempo]

    def obtener_necesidades(self):
        return self.necesidades
