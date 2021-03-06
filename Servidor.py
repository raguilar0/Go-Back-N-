#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Programa Servidor prueb
# Fuente original de este codigo: www.pythondiario.com
# Utilizado para fines academicos en el curso CI-1320 

#Modificado por Alejandro Córdoba Soto y Ricardo Aguilar Vargas
#Proyecto del curso CI-1320

import socket
import sys
import threading
 
# Creando el socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace de socket y puerto
puertoServidor = int(sys.argv[1])
modo = int(sys.argv[2])
server_address = ('localhost', puertoServidor)
print >>sys.stderr, 'empezando a levantar %s puerto %s' % server_address
sock.bind(server_address)
archivo = open('salida.txt', 'w')
ultimoAckEnviado = -1
lista_ack_pendientes = []
# Escuchando conexiones entrantes
sock.listen(1)
 
while True:
    # Esperando conexion
    print >>sys.stderr, 'Esperando para conectarse'
    connection, client_address = sock.accept()
    

    try:
        print >>sys.stderr, 'conexion desde', client_address 
 
        # Recibe los datos en trozos y reetransmite
        while True:
            data = connection.recv(7)
            print >>sys.stderr, 'recibido %s' % data
            pos = len(data)
            caracter = data[pos-1]
            seq = data[0:pos-2]
            ack = seq+':'+caracter
            archivo.write(caracter)
            if data:
                if (ultimoAckEnviado == (int(seq)-1)):
                    print >>sys.stderr, 'enviando ACK al cliente'+ack
                    connection.sendall(ack)
                    ultimoAckEnviado = int(seq)
                    if lista_ack_pendientes.count > 0:
                        i = len(lista_ack_pendientes)
                        for j in range (i):
                            l_data = lista_ack_pendientes.pop()
                            print 'LISTA [',j,' ] ', l_data
                            l_seq = l_data[0:pos-2]
                            if l_seq == ultimoAckEnviado - 1:
                                connection.sendall(l_data)
                                print >>sys.stderr, 'enviando ACK al cliente'+l_data
                            else:
                                lista_ack_pendientes.append(l_data)
                                lista_ack_pendientes.sort()

                else:
                    print 'No se puede enviar el ACK', ack
                    lista_ack_pendientes.append(data)
                    lista_ack_pendientes.sort()

            else:
                print >>sys.stderr, 'no hay mas datos', client_address
                break
             
    finally:
        # Cerrando conexion
        connection.close()
        archivo.close()
