<?xml version="1.0" encoding="utf-8"?>

<!-- ======================================================== -->
<!-- File    : PROTEUS_use_case.xsl                           -->
<!-- Content : PROTEUS XSLT for subjects at US - use case     -->
<!-- Author  : José María Delgado Sánchez                     -->
<!-- Date    : 2023/08/10                                     -->
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
    <!-- Use case template                              -->
    <!-- ============================================== -->
    <!-- Note the use of colspan=2                      -->

    <xsl:template match="object[@classes='product-requirement use-case']">
        <xsl:variable name="span" select="2" />

        <xsl:variable name="label_number">
            <xsl:number from="object[@classes='Proteus-document']"
                count="object[@classes='product-requirement use-case']"
                level="any" format="001" />
        </xsl:variable>

        <div id="{@id}">
            <table class="use_case remus_table">

                <xsl:call-template name="generate_expanded_header">
                    <xsl:with-param name="label" select="concat('UC-',$label_number)" />
                    <xsl:with-param name="class" select="'useCase'" />
                    <xsl:with-param name="span" select="$span" />
                </xsl:call-template>

                <!-- description -->
                <xsl:call-template name="generate_markdown_row">
                    <xsl:with-param name="label" select="$proteus:lang_description" />
                    <xsl:with-param name="content"
                        select="properties/markdownProperty[@name='description']" />
                    <xsl:with-param name="span" select="$span" />
                </xsl:call-template>

                <!-- precondition -->
                <xsl:call-template name="generate_markdown_row">
                    <xsl:with-param name="label" select="$proteus:lang_precondition" />
                    <xsl:with-param name="content"
                        select="properties/markdownProperty[@name='precondition']" />
                    <xsl:with-param name="span" select="$span" />
                </xsl:call-template>

                <!-- use case steps -->
                <!-- check if there are children otherwise do nothing -->
                <xsl:if test="children/object">
                    <!-- count the number of use case step in total -->
                    <xsl:variable name="number_of_steps" select="count(children/object)" />
                
                    <tr>
                        <th rowspan="{$number_of_steps + 1}">
                            <xsl:value-of select="$proteus:lang_ordinary_sequence" />
                        </th>
                        <th class="step_number_column">
                            <xsl:value-of select="$proteus:lang_step" />
                        </th>
                        <th class="step_action_column">
                            <xsl:value-of select="$proteus:lang_action" />
                        </th>
                    </tr>

                    <xsl:apply-templates select="children/object" />

                </xsl:if>

                <!-- postcondition -->
                <xsl:call-template name="generate_markdown_row">
                    <xsl:with-param name="label" select="$proteus:lang_postcondition" />
                    <xsl:with-param name="content"
                        select="properties/markdownProperty[@name='postcondition']" />
                    <xsl:with-param name="span" select="$span" />
                </xsl:call-template>

                <!-- comments -->
                <xsl:call-template name="generate_comments_row">
                    <xsl:with-param name="span" select="$span" />
                </xsl:call-template>

            </table>
        </div>
    </xsl:template>


    <!-- ============================================== -->
    <!-- Use case step template                         -->
    <!-- ============================================== -->

    <xsl:template match="object[@classes='product-requirement use-case use-case-step']">
        <xsl:variable name="label_number">
            <xsl:number from="object[@classes='product-requirement use-case']"
                count="object[@classes='product-requirement use-case use-case-step']"
                level="any" format="1" />
        </xsl:variable>

        <xsl:call-template name="generate_markdown_row">
            <xsl:with-param name="id" select="@id" />
            <xsl:with-param name="label" select="$label_number" />
            <xsl:with-param name="content"
                select="properties/markdownProperty[@name='description']" />
        </xsl:call-template>
    </xsl:template>

</xsl:stylesheet>