# 📝 Política de Commits

## 🎯 Objetivo

Padronizar as mensagens de commit, garantindo um histórico **limpo**, **rastreável** e que facilite a colaboração no projeto.

---

## 📦 Padrão Utilizado

Adotamos o modelo [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/), que organiza as mensagens seguindo a estrutura:

````bash
<tipo>(escopo): descrição breve
````

- `<tipo>`  O que você está fazendo (ex: feat, fix, docs, etc).
- `(escopo)` Área específica do código modificada.
- `descrição breve` Uma frase curta no tempo presente.

## 🏷️ Tipos de Commits Permitidos

| Tipo       | Descrição                                          | Exemplos de Uso |
|:-----------|:---------------------------------------------------|:----------------|
| `build`    | Ajustes em ferramentas ou dependências de build    | Configurar Docker, atualizar dependências do projeto |
| `static`   | Atualização de conteúdos estáticos                 | Substituir imagens, corrigir texto institucional |
| `ci`       | Alterações em processos de integração contínua     | Atualizar workflows de testes automáticos |
| `cd`       | Melhorias na entrega contínua                      | Ajustar rotinas de deploy automático |
| `docs`     | Mudanças apenas em documentação                    | Corrigir instruções de instalação no README |
| `feat`     | Desenvolvimento de uma nova funcionalidade         | Implementar login social, adicionar exportação em CSV |
| `fix`      | Correção de defeitos ou falhas no código            | Resolver problema de autenticação no mobile |
| `perf`     | Melhorias específicas de desempenho                | Reduzir tempo de carregamento da home page |
| `refactor` | Refatoração de código sem alterar o funcionamento  | Reestruturar controllers para melhor organização |
| `improve`  | Ajustes visuais ou melhorias pequenas              | Melhorar responsividade em dispositivos móveis |
| `style`    | Alterações de estilo de código                     | Aplicar formatação de código padrão, ajustes no ESLint |
| `test`     | Inclusão ou atualização de testes                  | Adicionar testes de integração para novo serviço |
| `revert`   | Reversão de mudanças anteriores                    | Desfazer atualização que causou erro em produção |

---

## ℹ️ Observações Importantes

- Use o tipo que **melhor descreva a natureza da alteração**.
- Caso tenha dúvidas, prefira abrir uma **issue** para discussão antes de submeter o commit.

---

## 📜 Regras de Mensagens de Commit

Para manter a consistência e a clareza no histórico de commits, siga estas regras:

- Comece sempre com um dos tipos permitidos (`feat`, `fix`, `docs`, etc.).
- Utilize escopo (entre parênteses) sempre que fizer sentido.
- Escreva a descrição no tempo presente e de forma objetiva.
- Não use descrições vagas como "ajustes" ou "mudanças".
- Cada commit deve representar uma alteração lógica isolada.
- Evite commits grandes demais: prefira mudanças menores e claras.
- Use `revert` caso precise desfazer um commit anterior.

---