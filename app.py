import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

markdown_text = "The Gender Wage gap is a controversial phenomenon in the US in which women are said to earn less in wages compared to men. This phenomenon has been explained by various source, some saying that the phenomenon disappears when occupation is controlled and some saying it is due to gender discrimination. Some sources, notably on today's Ameican political 'left' describe it as discrimination while the political 'right' describe it as attributable to other characterstics about people, not gender discrimination.\n The GSS is a national survey that is representative of adults in the US since 1972. Its goal is to collect data on American public opinion and explore trends and attitudes. The questions tend to be political and address various topics such as civil liberties, crime and violence, and morality.\nhttps://www.gss.norc.org/About-The-GSS\nhttps://www.americanprogress.org/article/quick-facts-gender-wage-gap/\nhttps://time.com/3222543/wage-pay-gap-myth-feminism/"

p2 = round(gss_clean.groupby('sex').agg({'income':'mean',
                              'job_prestige':'mean',
                              'education':'mean'}),2).reset_index().rename(columns={'income':'Mean Income',
                                                                      'job_prestige':'Mean Job Prestige',
                                                                      'education':'Mean Years of Education',
                                                                      'sex':'Sex'})
table = ff.create_table(p2)
p3 = gss_clean.groupby(['sex', 'male_breadwinner']).size().reset_index().rename(columns={'sex':'Sex',
                                                                                         'male_breadwinner':'Agreement with the Male Breadwinner Question',
                                                                                         0:'Count'})
fig3 = px.bar(p3, x='Agreement with the Male Breadwinner Question', 
             y='Count', color='Sex',
            title = 'Counts of Agreement with Breadwinner Question by Gender',
            barmode = 'group')
fig3.update_layout(showlegend=True)
fig3.update(layout=dict(title=dict(x=0.5)))
fig4 = px.scatter(gss_clean, x='job_prestige', y='income', 
                 color = 'sex', trendline='ols',
                 labels={'job_prestige':'Job Prestige', 
                        'income':'Income',
                        'sex':'Sex'},
                 hover_data=['education', 'socioeconomic_index'],
                 title = 'Income vs. Job Prestige by Sex')
fig4.update(layout=dict(title=dict(x=0.5)))
fig5_1 = px.box(gss_clean, x='sex', y='income', labels={'sex':'Sex',
                                                        'income':'Income'}, 
                title='Distribution of Income by Sex')
fig5_1.update(layout=dict(title=dict(x=0.5)))
fig5_2 = px.box(gss_clean, x='sex', y='job_prestige', labels={'sex':'Sex',
                                                        'job_prestige':'Job Prestige'}, 
                title='Distribution of Job Prestige by Sex')
fig5_2.update(layout=dict(title=dict(x=0.5)))
p6 = gss_clean[['income', 'sex', 'job_prestige']]
p6['job_prestige_group'] = pd.cut(p6['job_prestige'], 6)
p6 = p6.dropna()
fig = px.box(p6, x='sex', y='income', color='sex',
             facet_col='job_prestige_group', facet_col_wrap=3,
            labels={'sex':'Sex', 'income':'Income',
                    'job_prestige_group':'Job Prestige Category'},
            title = 'Income by Sex and Job Prestige Group',
            width=900, height=600)
fig.update(layout=dict(title=dict(x=0.5)))
fig.update_layout(showlegend=True)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    [
        html.H1("Exploring the Gender Wage Gap"),
        
        dcc.Markdown(children = markdown_text),
        
        html.H2("Table of Mean Income, Job Prestige, and Education Years by Gender"),
        
        dcc.Graph(figure=table),
        
        html.H2("Barplots of Responses to Breadwinner Question by Gender"),
        
        dcc.Graph(figure=fig3),
        
        html.H2("Scatterplot of Income vs. Job Prestige by Sex"),
        
        dcc.Graph(figure=fig4),
        
        html.H2("Boxplot of Income by Sex"),
        
        dcc.Graph(figure=fig5_1),
        
        html.H2("Boxplot of Job Prestige by Sex"),
        
        dcc.Graph(figure=fig5_2),
        
        html.H2("Faceted Boxplots of Income by Sex and Job Prestige"),
        
        dcc.Graph(figure=fig),
    
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
