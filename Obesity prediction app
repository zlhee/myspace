library(caret)
library(shiny)
library(LiblineaR)
library(readr)
library(ggplot2)
library(shiny)
library(shinydashboard)
library(shinythemes)



# model
model2 = train(target~., 
               data = x_train_scaled, 
               method = "ranger", 
               trControl = train_control2,
               tuneGrid = ranger_tune_grid)
model2

save(model2 , file = 'ranger.rda')
source("cst_model.R")

server <- shinyServer(function(input, output) {
  
  options(shiny.maxRequestSize = 800*1024^2)   # This is a number which specifies the maximum web request size, 
  # which serves as a size limit for file uploads. 
  # If unset, the maximum request size defaults to 5MB.
  # The value I have put here is 80MB
  
  
  output$sample_input_data_heading = renderUI({   # show only if data has been uploaded
    inFile <- input$file1
    
    if (is.null(inFile)){
      return(NULL)
    }else{
      tags$h4('Sample data')
    }
  })
  
  output$sample_input_data = renderTable({    # show sample of uploaded data
    inFile <- input$file1
    
    if (is.null(inFile)){
      return(NULL)
    }else{
      input_data =  readr::read_csv(input$file1$datapath, col_names = TRUE)
      
      colnames(input_data) = c('region','sex','age','occp','allownc','marri_1','marri_2','DI1_dg',
                               'DI2_dg','DM1_dg','DM2_dg','DE1_dg','DC7_dg','DM8_dg','HE_BMI','LQ_1EQL',
                               'educ','BO1','BD1_11','BP1','BS3_1','L_BR_FQ','L_LN_FQ','L_DN_FQ',
                               'HE_sbp1','HE_dbp1','HE_glu','HE_HbA1c','HE_insulin','HE_chol','HE_Uacid','N_WATER'
      )
      
      input_data$HE_BMI = as.factor(input_data$HE_BMI )
      
      levels(input_data$HE_BMI) <- c("저체중","정상","비만 전단계","비만 1단계","비만 2단계","비만 3단계")
      head(input_data)
    }
  })
  
  
  
  predictions<-reactive({
    
    inFile <- input$file1
    
    if (is.null(inFile)){
      return(NULL)
    }else{
      withProgress(message = 'Predictions in progress. Please wait ...', {
        input_data =  readr::read_csv(input$file1$datapath, col_names = TRUE)
        
        colnames(input_data) = c('region','sex','age','occp','allownc','marri_1','marri_2','DI1_dg',
                                 'DI2_dg','DM1_dg','DM2_dg','DE1_dg','DC7_dg','DM8_dg','HE_BMI','LQ_1EQL',
                                 'educ','BO1','BD1_11','BP1','BS3_1','L_BR_FQ','L_LN_FQ','L_DN_FQ',
                                 'HE_sbp1','HE_dbp1','HE_glu','HE_HbA1c','HE_insulin','HE_chol','HE_Uacid','N_WATER')
        
        input_data$HE_BMI = as.factor(input_data$HE_BMI )
        
        levels(input_data$HE_BMI) <- c("저체중","정상","비만 전단계","비만 1단계","비만 2단계","비만 3단계")
        
        prediction = predict(model2,x_test_scaled)
        
        result = sum(as.factor(pred_y)==y_test)/nrow(x_test_scaled)*100
        result
        
      })
    }
  })
  
  
  output$sample_prediction_heading = renderUI({  # show only if data has been uploaded
    inFile <- input$file1
    
    if (is.null(inFile)){
      return(NULL)
    }else{
      tags$h4('Sample predictions')
    }
  })
  
  output$sample_predictions = renderTable({   # the last 6 rows to show
    pred = predictions()
    head(pred)
    
  })
  
  
  output$plot_predictions = renderPlot({   # the last 6 rows to show
    pred = predictions()
    cols <- c("저체중" = "green","정상" = "blue","비만 경고" = "yellow", "비만 위험" = "red")
    
  })
  
  
  # Downloadable csv of predictions ----
  
  output$downloadData <- downloadHandler(
    filename = function() {
      paste("input_data_with_predictions", ".csv", sep = "")
    },
    content = function(file) {
      write.csv(predictions(), file, row.names = FALSE)
    })
  
})



ui <- dashboardPage(skin="black",
              dashboardHeader(title=tags$em("Obesity prediction app", style="text-align:center;color:#006600;font-size:100%"),titleWidth = 800),
              
              dashboardSidebar(width = 250,
                               sidebarMenu(
                                 br(),
                                 menuItem(tags$em("Upload Test Data",style="font-size:120%"),icon=icon("upload"),tabName="data"),
                                 menuItem(tags$em("Download Predictions",style="font-size:120%"),icon=icon("download"),tabName="download")
                                 
                                 
                               )
              ),
              
              dashboardBody(
                tabItems(
                  tabItem(tabName="data",
                          
                          
                          br(),
                          br(),
                          br(),
                          br(),
                          tags$h4("Note: All BMI information is based on the Korea National Health & Nutrition Examination Survey. This data does not collect personal information.", style="font-size:150%"),
                          
                          
                          br(),
                          
                          tags$h4("To predict using this model, upload test data in csv format (you can change the code to read other data types) by using the button below.", style="font-size:150%"),
                          
                          tags$h4("Then, go to the", tags$span("Download Predictions",style="color:red"),
                                  tags$span("section in the sidebar to download the predictions."), style="font-size:150%"),
                          
                          br(),
                          br(),
                          br(),
                          column(width = 4,
                                 fileInput('file1', em('Upload test data in csv format ',style="text-align:center;color:blue;font-size:150%"),multiple = FALSE,
                                           accept=c('.csv')),
                                 
                                 uiOutput("sample_input_data_heading"),
                                 tableOutput("sample_input_data"),
                                 
                                 
                                 br(),
                                 br(),
                                 br(),
                                 br()
                          ),
                          br()
                          
                  ),
                  
                  
                  tabItem(tabName="download",
                          fluidRow(
                            br(),
                            br(),
                            br(),
                            br(),
                            column(width = 8,
                                   tags$h4("After you upload a dataset, you can download the predictions in csv format by
                                    clicking the button below.", 
                                           style="font-size:200%"),
                                   br(),
                                   br()
                            )),
                          fluidRow(
                            
                            column(width = 7,
                                   downloadButton("downloadData", em('Download Predictions',style="text-align:center;color:blue;font-size:150%")),
                                   plotOutput('plot_predictions')
                            ),
                            column(width = 4,
                                   uiOutput("sample_prediction_heading"),
                                   tableOutput("sample_predictions")
                            )
                            
                          ))
                )))

shinyApp(ui,server)
