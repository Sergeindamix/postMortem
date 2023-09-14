import streamlit as st
import re
from datetime import datetime

def fill_contract_template(contract_text, fill_values):
    for placeholder, value in fill_values.items():
        contract_text = contract_text.replace(placeholder, value)
    return contract_text

def main():
    st.title("Generador de Contrato de Arrendamiento")

    # Contrato de arrendamiento con campos de relleno
    contract_template = """
    CONTRATO DE ARRENDAMIENTO PARA EL EDO. DE MEXICO PARA CASA HABITACION O NEGOCIO 

    De acuerdo con lo dispuesto en el Artículo 2560 del Código Civil del Estado de México, celebran el .presente contrato de Arrendamiento, el arrendador(a) {arrendador} da en arrendamiento al Sr(a) {arrendatario} la casa ubicada en la calle Primero de Mayo con número  12 y 13, en la colonia Plan de Ayala 2a, C.P. 53710 sujetándose a las siguientes cláusulas:

    PRIMERA. - El arrendatario pagará al arrendador o a quien sus derechos represente, la cantidad de ${0000}  ( {cantidad} ) por el arrendamiento mensual de la localidad mencionada arriba, que se cubrirá en moneda del cuño nacional con toda puntualidad al arrendador o de quien sus derechos represente, de acuerdo con lo que previenen los artículos 2279 y 2281. 

    SEGUNDA.- De acuerdo al artículo 2283 el arrendatario está obligado a pagar la renta que se venza hasta el día que entregué la casa arrendada 

    TERCERA.- El inicio del arrendamiento será a partir de la fecha  {fechaInicio} y concluirá el {fechaFinal}

    CUARTA.- El arrendatario no podrá traspasar o subarrendar la localidad arrendada y en caso de hacerlo será con permiso y por escrito del arrendador 

    QUINTA. - Si el arrendatario recibió la finca con expresa descripción de las partes que se compone, debe devolverla, al concluir el arrendamiento, tal como la recibió, salvo lo que hubiese perecido o se hubiere menoscabado por el tiempo por causa inevitable, de acuerdo al Artículo 2296. 

    SEXTA.- De acuerdo al Artículo 2295, el arrendatario no puede, sin consentimiento expreso del arrendador, variar la forma de la finca, y si lo hace, cuando la devuelva deberá restablecerla, siendo, además responsable de los daños y perjuicios.

    SEPTIMA.- El arrendatario hará uso de la casa únicamente para habitación, si infringiere esta cláusula se dará por rescindido dicho contrato.

    OCTAVA.-De acuerdo al Artículo 2266, Fracción I, II, III el arrendador está obligado a entregar al arrendatario la finca arrendada con todas sus pertenencias y en estado de servir para el uso convenido; así como las condiciones que ofrezcan al arrendatario la higiene y seguridad del inmueble, así como también, a conservar la casa arrendada en el mismo estado, durante el arrendamiento, haciendo para ello todas las reparaciones necesarias y a no estorbar de manera alguna el uso de la casa arrendada, a no ser por causa de reparaciones urgentes e indispensables.

    NOVENA.-. El arrendatario deberá cuidar de no tener substancias corrosivas, material inflamable o peligroso y de ser así, deberá observar las leyes que regulen el manejo adecuado de dichas substancias según al Articulo 2294.
    DÉCIMA. De acuerdo a lo previsto en el Artículo 2298 el arrendatario debe hacer las reparaciones de aquellos deterioros de poca importancia, que regularmente son causados, por las personas que habitan la finca o estructura.

    DECIMA PRIMERA.- El arrendador no puede, durante el arrendamiento mudar la forma de la finca ni intervenir en el uso legítimo de ella, por su parte, el arrendatario está obligado a poner el conocimiento del arrendador, a la brevedad posible, la necesidad de las reparaciones, bajo pena de pagar los daños y perjuicios que su omisión cause, si el arrendador no cumpliere con hacer las reparaciones necesarias para el uso que está destinada la finca, quedará a elección del arrendatario rescindir el arrendamiento u ocurrir al juez para que estreche al arrendador para dar cumplimiento de su obligación, Articulo 2268, 22'79 y 2299. 

    DECIMA  SEGUNDA.- Para garantizar el cumplimiento de este contrato entrega el arrendatario la cantidad de: $ {0000} ({pesos}) la cual se devolverá cuando desocupe la localidad siempre que no deba nada por renta, según constancia por escrito del arrendador. 

    DECIMA TERCERA.- Para garantizar el cumplimiento de este contrato firma como aval el Sr. (a)  N/A
    Y señala como su domicilio la calle N/A
    Colonia N/A
    C.P.N/A
    Ciudad  N/A
    Tel. N/A
    la cual se identifica con credencial de: N/A
    con Folio No. N/A

    DÉCIMA CUARTA.- Ambas partes establecen que el presente contrato de arrendamiento concluya el día prefijado y cuando este no sea por tiempo determinado, cada una de las partes lo dará por terminado previo aviso con quince días de anticipación. 

    DÉCIMA QUINTA.- En caso de alguna controversia ambas partes se apegan al Código Civil vigente en el Edo. de México.
    Las parte contratantes, perfectamente enteradas del contenido y alcance de todas y cada una de las cláusulas anteriores, firman el presente contrato y están conformes en que el presente contrato empiece a regir.

    
    EN EL ESTADO DE MEXICO, A: {FECHA}

    FIRMAS:

    _______________________           ___________________________
    El arrendador                     El arrendatario
    {arrendador}                      {arrendatario}
    """

    # Mostrar el contrato con campos de relleno
    st.subheader("Contrato de Arrendamiento:")
    st.text(contract_template)

    # Campos de relleno
    fill_values = {
        "{arrendador}": st.text_input("Nombre del arrendador:"),
        "{arrendatario}": st.text_input("Nombre del arrendatario:"),
        "{cantidad}": st.text_input("Cantidad de renta:"),
        "{fechaInicio}": st.text_input("Fecha de inicio:"),
        "{fechaFinal}": st.text_input("Fecha de finalización:")
        # Agregar más campos aquí
    }

    # Obtener la fecha actual
    current_date = datetime.now().strftime("%d/%m/%Y")
    fill_values["{FECHA}"] = current_date

    if all(value for value in fill_values.values()):
        filled_contract = fill_contract_template(contract_template, fill_values)
        st.subheader("Contrato de Arrendamiento Rellenado:")
        st.text(filled_contract)

if __name__ == "__main__":
    main()
