package com.example.demo.app;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller 
public class ViewController {

    @GetMapping("/")
    public String home(Model model) {
        model.addAttribute("title", "스트리밍 데모");
        return "index";
    }
}
