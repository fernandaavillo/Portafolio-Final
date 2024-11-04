# Verificar e instalar paquete necesario
if (!requireNamespace("stats", quietly = TRUE)) {
  install.packages("stats")
}

# Función de Black-Scholes para opciones europeas
black_scholes <- function(S, K, r, sigma, T, tipo = "call") {
  # S: Precio del activo subyacente
  # K: Precio de ejercicio
  # r: Tasa libre de riesgo
  # sigma: Volatilidad del activo
  # T: Tiempo hasta el vencimiento en años
  # tipo: "call" o "put"
  
  d1 <- (log(S / K) + (r + (sigma^2) / 2) * T) / (sigma * sqrt(T))
  d2 <- d1 - sigma * sqrt(T)
  
  if (tipo == "call") {
    # Fórmula para opción call
    valor <- S * pnorm(d1) - K * exp(-r * T) * pnorm(d2)
  } else if (tipo == "put") {
    # Fórmula para opción put
    valor <- K * exp(-r * T) * pnorm(-d2) - S * pnorm(-d1)
  } else {
    stop("El tipo debe ser 'call' o 'put'")
  }
  
  return(valor)
}

# Función para limpiar y validar entradas del usuario
validar_entrada <- function(entrada) {
  valor <- suppressWarnings(as.numeric(entrada))
  if (is.na(valor)) {
    stop("Entrada inválida. Asegúrese de ingresar un número válido.")
  }
  return(valor)
}

# Función principal para solicitar parámetros y valorizar opción
valorizar_opcion <- function() {
  cat("----- Valorización de Opción Europea (Modelo Black-Scholes) -----\n")
  
  # Solicitar entradas y limpiarlas/transformarlas
  S <- validar_entrada(readline("Ingrese el precio del activo subyacente (S): "))
  K <- validar_entrada(readline("Ingrese el precio de ejercicio (K): "))
  r <- validar_entrada(readline("Ingrese la tasa libre de riesgo (r, en decimal, ej. 0.05 para 5%): "))
  sigma <- validar_entrada(readline("Ingrese la volatilidad (sigma, en decimal, ej. 0.2 para 20%): "))
  T <- validar_entrada(readline("Ingrese el tiempo hasta el vencimiento en años (T): "))
  tipo <- tolower(readline("Ingrese el tipo de opción ('call' o 'put'): "))
  
  # Validar el tipo de opción
  if (!(tipo %in% c("call", "put"))) {
    stop("El tipo de opción debe ser 'call' o 'put'.")
  }
  
  # Calcular el valor de la opción
  resultado <- black_scholes(S, K, r, sigma, T, tipo)
  
  # Mostrar el resultado
  cat("El valor de la opción", tipo, "es:", round(resultado, 4), "\n")
}

# Ejecutar la función principal
valorizar_opcion()

library(shiny)

ui <- fluidPage(
  titlePanel("Valorización de Opciones - Modelo Black-Scholes"),
  sidebarLayout(
    sidebarPanel(
      numericInput("S", "Precio del activo subyacente (S):", value = 100),
      numericInput("K", "Precio de ejercicio (K):", value = 105),
      numericInput("r", "Tasa libre de riesgo (r):", value = 0.05),
      numericInput("sigma", "Volatilidad (sigma):", value = 0.2),
      numericInput("T", "Tiempo al vencimiento (T, años):", value = 1),
      selectInput("tipo", "Tipo de opción:", choices = c("call", "put"))
    ),
    mainPanel(
      textOutput("resultado")
    )
  )
)

server <- function(input, output) {
  output$resultado <- renderText({
    resultado <- black_scholes(input$S, input$K, input$r, input$sigma, input$T, input$tipo)
    paste("El valor de la opción", input$tipo, "es:", round(resultado, 4))
  })
}

shinyApp(ui = ui, server = server)

