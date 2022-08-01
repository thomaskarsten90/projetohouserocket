# Projeto House Rocket (Empresa fictícia de compra e venda de Imóveis)

Este projeto é sobre uma empresa fictícia que tem como obejtivo comprar imóveis num preço mais baixo da média de preços da região e vendê-los posteriormente por um preço maior visando o maior lucro possível.

Juntamente com a conclusão final de quais imóveis são recomendados para compra, foi fornecido para o time de negócios 10 hipósteses para que possa gerar insights.

O projeto foi disponibilizado para visualização através da ferramenta Streamlit, que permite que o time de negócio acesse do seu computador pessoal, tablet ou smarthphone.

Link para visualização:  https://projeto-de-analise-houserocket.herokuapp.com/

## Sobre a House Rocket

A House Rocket é uma empresa do ramo imbiliário que tem como objetivo a compra e venda de imóveis.

A principal estratégia da empresa é ***comprar boas casas*** em ótimas localizações e com preços abaixo da média da região para depois revendê-las com preços mais altos. 

Neste projeto, foi encontrado o melhor preço para a venda das casa e também a melhor epoca do ano para vendê-las.


## Questão do negócio:

O projeto busca responder às seguintes perguntas de negócio, feitas pelo CEO da empresa:

- Quais são os imóveis que a House Rocket deveria comprar e por qual preço?
- Uma vez a casa comprada, qual o melhor momento para vendê-las e por qual preço?

As respostas a essas perguntas foram disponibilizadas no link acima usando o streamlit para uma melhor visualização.

## Premissas do projeto

Para a execução deste projeto algumas premissas foram adotadas, sendo elas:

* Os valores iguais a zero em yr_renovated são casas que nunca foram reformadas;
* O valor igual a 33 na coluna bathroom foi considerada um erro e por isso foi deletada das análises.
* A coluna price significa o preço que a casa foi ou será comprada pela empresa House Rocket;
* Valores duplicados em id foram removidos e considerados somente a compra mais recente;
* Dado que a localidade e a condição são os principais fatores que influenciam na valorização ou desvalorização dos imóveis, essas foram características decisivas na seleção ou não dos imóveis;
* Para as condições dos imóveis, foi determinada a seguinte classificação: 1 e 2 = bad, 3 e 4 = regular e 5 = good;
* Como a sazonalidade também influencia diretamente a demanda por investimento em imóveis, a estação do ano foi decisiva para a época da venda do imóvel; 
* O time de negócios aplicará o percentual de 30% sobre o valor dos imóveis que forem comprados abaixo do valor mediano da região + sazonalidade, e de 10% nos imóveis comprados acima do valor mediano da região + sazonalidade.

## 6. Resultado financeiro

O objetivo desse projeto é fornecer uma lista de imóveis com opções de compra e venda, para obtenção do __lucro máximo__ que poderá ser obtido se todas as sugestões ocorrerem. O resultado financeiro apresentado representa o lucro máximo que pode ser obtido utilizando as recomendações informadas.

| __Número de imóveis__ | __Custo total__ | __Receita de vendas__ | __Lucro (profit)__ |
| ----------------- | ----------------- | ----------------- | ----------------- |
| 10.642 | R$ 4.079.586.744,00 | R$ 4.766.745.551,20 | R$ 687.158.807,20 |


## 6. Conclusão

O objetivo deste projeto é prover para o time de negócio informações suficientes para uma melhor tomada de decisões. Sendo assim, este projeto cumpriu sua função.
