<?xml version="1.0" encoding="utf-8"?>


<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    xmlns:proteus-utils="http://proteus.us.es/utils"
    exclude-result-prefixes="proteus proteus-utils"
>

<xsl:template match="object[@classes='uml class-diagram']">
    <div>
        <xsl:variable name="plantUmlCode" select="proteus-utils:generate_class_diagram(@id)"/>
        <xsl:variable name="objectId" select="@id" />

        <xsl:value-of select="$plantUmlCode"/>

        <img class="figure_image proteus-area" id="{@id}"></img>

        
        <script>
            document.addEventListener('DOMContentLoaded', function () {
                displayPlantUMLDiagram(`<xsl:value-of select="$plantUmlCode" />`, `<xsl:value-of select="$objectId" />`);
            });
        </script>

    </div>



</xsl:template>

</xsl:stylesheet>