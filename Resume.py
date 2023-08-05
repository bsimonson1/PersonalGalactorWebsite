import pygame
import fitz

class Resume():
    @staticmethod
    def render_pdf(screen, clock, pdf_path):
        pdf_document = fitz.open(pdf_path)

        # The following loop will render each page of the PDF
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            image = page.get_pixmap()
            mode = "RGB" if image.n >= 3 else "P"
            image_surface = pygame.image.fromstring(image.samples, (image.width, image.height), mode)
            screen.blit(image_surface, (0, 0))

            pygame.display.flip()
            clock.tick(10)  # Set a delay to slow down the rendering (adjust as needed)

        pdf_document.close()

    @staticmethod
    def resume_render():
        pygame.init()

        # Set the dimensions of your window
        window_width = 800
        window_height = 600

        # Create the window
        screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Resume")
        clock = pygame.time.Clock()

        # Replace 'path/to/your/pdf/file.pdf' with the actual path to your PDF file
        pdf_file_path = "C:\\Users\\bengs\\OneDrive\\Documents\\Personal_Docs\\Benjamin_SimonsonResume.pdf"
        Resume.render_pdf(screen, clock, pdf_file_path)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
            pygame.display.update()
            clock.tick(60)  # Set the frame rate (adjust as needed)

        pygame.quit()
