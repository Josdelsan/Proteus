<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_objective.xsl                          -->
<!-- Content : PROTEUS XSLT for subjects at US - objective    -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/08/02                                     -->
<!-- Version : 1.0                                            -->
<!-- ======================================================== -->

<!-- ======================================================== -->
<!-- exclude-result-prefixes="proteus" must be set in all     -->
<!-- files to avoid xmlsn:proteus="." to appear in HTML tags. -->
<!-- ======================================================== -->

<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:proteus="http://proteus.us.es"
    exclude-result-prefixes="proteus"
>

    <!-- ============================================== -->
    <!-- Objective template                             -->
    <!-- ============================================== -->
    <!-- Note the use of colspan=2                      -->

    <xsl:template match="object[@classes='objective']">
        <xsl:variable name="span" select="2" />

        <xsl:variable name="label_number">
            <xsl:number from="object[@classes='Proteus-document']"
                count="object[@classes='objective']"
                level="any" format="001" />
        </xsl:variable>

        <div id="{@id}">
            <table class="objective remus_table">

                <xsl:call-template name="generate_expanded_header">
                    <xsl:with-param name="label" select="concat('OBJ-',$label_number)" />
                    <xsl:with-param name="class" select="'objective'" />
                    <xsl:with-param name="span" select="$span" />
                </xsl:call-template>

                <!-- description -->
                <xsl:call-template name="generate_markdown_row">
                    <xsl:with-param name="label" select="$proteus:lang_description" />
                    <xsl:with-param name="content"
                        select="properties/markdownProperty[@name='description']" />
                    <xsl:with-param name="span" select="$span" />
                </xsl:call-template>

                <!-- subobjectives -->
                <!-- check if there are children otherwise do nothing -->
                <xsl:if test="children/object">
                    <tr>
                        <th>
                            <xsl:value-of select="$proteus:lang_subobjectives" />
                        </th>
                        <td colspan="{$span}">
                            <ul class="subobjectives">
                                <xsl:for-each select="children/object">
                                    <xsl:call-template name="generate_subobjective"/>
                                </xsl:for-each>
                            </ul>
                        </td>
                    </tr>
                </xsl:if>


                <xsl:call-template name="generate_comments_row">
                    <xsl:with-param name="span" select="$span" />
                </xsl:call-template>

            </table>
        </div>
    </xsl:template>


    <!-- ============================================== -->
    <!-- Subobjective template                          -->
    <!-- ============================================== -->

    <xsl:template name="generate_subobjective">
        <!-- Label number -->
        <xsl:variable name="label_number">
            <xsl:number from="object[@classes='Proteus-document']"
                count="object[@classes='objective']"
                level="any" format="001" />
        </xsl:variable>

        <div id="{@id}">
            <!-- Current objective -->
            <li>
                <strong>
                    <xsl:value-of select="concat('[OBJ-',$label_number,']')" />
                    <xsl:text> </xsl:text>
                    <xsl:value-of select="properties/stringProperty[@name=':Proteus-name']" />
                </strong>
                <xsl:text> : </xsl:text>
                <xsl:value-of select="properties/markdownProperty[@name='description']" />
            </li>

            <!-- Nested objectives -->
            <xsl:if test="children/object">
                <ul class="subobjectives">
                    <xsl:for-each select="children/object">
                        <xsl:call-template name="generate_subobjective"/>
                    </xsl:for-each>
                </ul>
            </xsl:if>
        </div>
    </xsl:template>

</xsl:stylesheet>